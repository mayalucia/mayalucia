;;; spirit-session.el --- Spirit-aware agent-shell session launch -*- lexical-binding: t; -*-
;;
;; Mechanism: wires spirit identity to agent-shell sessions.
;; Not a power, not a skill — plain harness plumbing owned by mayadev.
;;
;; Installation: source from ~/.doom.d/config.org (or equivalent) inside
;; (use-package! agent-shell :config ...).
;;
;; Convention: each project directory that has a guardian spirit places a
;; .guardian/identity file containing the spirit's true-name (one line,
;; plain text). This file is the filesystem-level identity marker — no
;; YAML parsing, no central registry lookup.
;;
;; Substrate resolution: .guardian/substrates/<backend>.yaml binds a
;; spirit to a specific LLM backend. .guardian/substrates/default names
;; the default backend (falls back to "claude"). The spirit is substrate-
;; agnostic; the harness resolves the binding at session launch.

;; Spirit color palette — mahābhūta (five elements)
;; Each guild maps to an element; spirits within a guild differentiate
;; by luminance (sattva=bright/primary, rajas=medium, tamas=dim).
;;
;; mayalucia (ākāśa/space)  — violet/indigo
;; bravli    (agni/fire)    — saffron/amber
;; epistem   (pṛthvī/earth) — ochre/warm-brown
;; apprentis (vāyu/wind)    — teal/cyan
(defvar agent-shell--spirit-colors
  '(;; guild          spirit               fg-dark       fg-light
    ;;
    ;; ākāśa (space) — luminous violet/lavender
    ;; Hue family: modus #caa6df (tags), #f78fe7 (type), #ff9bff (code)
    ("mayalucia"      "mayadev"            "#efbfff"     "#7b2fa0")
    ("mayalucia"      "sutradhar-guardian"  "#82e0aa"     "#2d6a1c")
    ("mayalucia"      "cruvin-guardian"     "#dcb5ff"     "#7b4f8a")
    ("mayalucia"      "dixa"               "#c4b0f0"     "#5b4a8a")
    ;;
    ;; agni (fire) — bright saffron/flame
    ;; Hue family: modus #ff925a (link), #ff5f59 (keyword)
    ("bravli"         "dmt-eval-guardian"   "#ffb070"     "#b85520")
    ;;
    ;; pṛthvī (earth) — warm gold/amber
    ;; Hue family: modus #ffdd00 (warning), #efcab2 (heading-2)
    ("epistem"        "epistem-guardian"    "#ffe080"     "#8a6d20")
    ("epistem"        "aikosh-guardian"     "#f5d060"     "#7a5c10")
    ;;
    ;; vāyu (wind) — bright cyan/sky
    ;; Hue family: modus #00d3d0 (builtin), #00bcff (variable)
    ("apprentis"      nil                  "#60f0f0"     "#1a7a88"))
  "Spirit color alist: (guild spirit fg-dark fg-light).
nil spirit matches any unregistered spirit in that guild.")

(defun agent-shell--spirit-color (name)
  "Return foreground color for spirit NAME based on guild and theme."
  (let* ((is-dark (eq (frame-parameter nil 'background-mode) 'dark))
         (entry (or (seq-find (lambda (e) (equal (nth 1 e) name))
                              agent-shell--spirit-colors)
                    ;; fallback: first guild-nil entry, or generic
                    (car (last agent-shell--spirit-colors))))
         (color (if is-dark (nth 2 entry) (nth 3 entry))))
    (or color (if is-dark "#b48ead" "#68217a"))))

(defun agent-shell--guardian-root ()
  "Find project root containing .guardian/identity, walking up from `default-directory'."
  (locate-dominating-file default-directory ".guardian/identity"))

(defun agent-shell--guardian-name ()
  "Read spirit name from .guardian/identity, walking up from `default-directory'."
  (when-let* ((root (agent-shell--guardian-root))
              (id-file (expand-file-name ".guardian/identity" root)))
    (string-trim
     (with-temp-buffer
       (insert-file-contents id-file)
       (buffer-string)))))

(defun agent-shell--spirit-identity-text ()
  "Read identity.yaml from .guardian/ at guardian root, or nil."
  (when-let* ((root (agent-shell--guardian-root))
              (id-path (expand-file-name ".guardian/identity.yaml" root))
              ((file-exists-p id-path)))
    (with-temp-buffer
      (insert-file-contents id-path)
      (buffer-string))))

(defun agent-shell--darken-color (hex factor)
  "Darken HEX color by FACTOR (0.0=black, 1.0=unchanged)."
  (let ((r (string-to-number (substring hex 1 3) 16))
        (g (string-to-number (substring hex 3 5) 16))
        (b (string-to-number (substring hex 5 7) 16)))
    (format "#%02x%02x%02x"
            (round (* r factor))
            (round (* g factor))
            (round (* b factor)))))

(defun agent-shell--blend-toward-bg (hex amount)
  "Blend HEX toward the frame background by AMOUNT (0.0=unchanged, 1.0=bg).
Produces a tinted background that is visible against the frame background."
  (let* ((bg (color-name-to-rgb (face-background 'default)))
         (r (string-to-number (substring hex 1 3) 16))
         (g (string-to-number (substring hex 3 5) 16))
         (b (string-to-number (substring hex 5 7) 16))
         (bg-r (round (* (nth 0 bg) 255)))
         (bg-g (round (* (nth 1 bg) 255)))
         (bg-b (round (* (nth 2 bg) 255))))
    (format "#%02x%02x%02x"
            (round (+ (* r (- 1 amount)) (* bg-r amount)))
            (round (+ (* g (- 1 amount)) (* bg-g amount)))
            (round (+ (* b (- 1 amount)) (* bg-b amount))))))

;; --- Substrate resolution ---

(defun agent-shell--default-substrate ()
  "Read the default substrate name from .guardian/substrates/default.
Falls back to \"claude\" if the file does not exist."
  (let* ((root (agent-shell--guardian-root))
         (default-file (when root
                         (expand-file-name ".guardian/substrates/default" root))))
    (if (and default-file (file-exists-p default-file))
        (string-trim
         (with-temp-buffer
           (insert-file-contents default-file)
           (buffer-string)))
      "claude")))

(defun agent-shell--default-substrate-p (backend)
  "Return non-nil if BACKEND is the project's default substrate."
  (string-equal backend (agent-shell--default-substrate)))

(defun agent-shell--available-substrates ()
  "List available substrate names from .guardian/substrates/*.yaml."
  (when-let* ((root (agent-shell--guardian-root))
              (dir (expand-file-name ".guardian/substrates/" root))
              ((file-directory-p dir)))
    (mapcar #'file-name-sans-extension
            (directory-files dir nil "\\.yaml\\'"))))

(defun agent-shell--client-maker-for-backend (backend)
  "Return a client-maker lambda for BACKEND string."
  (pcase backend
    ("gemini" (lambda (buffer)
               (agent-shell-google-make-gemini-client :buffer buffer)))
    ("codex"  (lambda (buffer)
               (agent-shell-openai-make-codex-client :buffer buffer)))
    (_        (lambda (buffer)
               (agent-shell-anthropic-make-claude-client :buffer buffer)))))

;; --- Banner ---

(defun agent-shell--format-spirit-banner (name identity-text &optional substrate-info)
  "Format a welcome banner for spirit NAME with IDENTITY-TEXT.
SUBSTRATE-INFO, if non-nil, is a string like \"claude-opus-4-6\" shown
in the banner. Uses `font-lock-face' (not `face') so properties survive
comint output filter."
  (let* ((color (agent-shell--spirit-color name))
         (bg (agent-shell--blend-toward-bg color 0.75))
         (header-face `(:foreground ,color :background ,bg :weight bold))
         (box-face `(:foreground ,color))
         (dim-face `(:foreground ,color :weight light)))
    (concat "\n"
            (if identity-text
                (concat (propertize (concat "  ┌─ " name " ─────────────────────────  ")
                                    'font-lock-face header-face)
                        "\n"
                        (mapconcat (lambda (line)
                                    (concat (propertize "  │ " 'font-lock-face box-face)
                                            (propertize line 'font-lock-face dim-face)))
                                  (split-string identity-text "\n")
                                  "\n")
                        (when substrate-info
                          (concat "\n"
                                  (propertize "  │ " 'font-lock-face box-face)
                                  (propertize (concat "substrate: " substrate-info)
                                              'font-lock-face dim-face)))
                        "\n"
                        (propertize "  └──────────────────────────────────" 'font-lock-face box-face)
                        "\n")
              (propertize (format "  Spirit: %s (no identity.yaml found)\n" name)
                          'font-lock-face dim-face)))))

(defun agent-shell--spirit-welcome (name &optional substrate-info)
  "Return a welcome function for spirit NAME.
SUBSTRATE-INFO is an optional string (e.g. model name) shown in the banner.
Captures plain data eagerly; builds propertized banner at display time
so text properties survive (backquote splicing strips them)."
  (let ((id-text (agent-shell--spirit-identity-text)))
    `(lambda (_config)
       (agent-shell--format-spirit-banner ,name ,id-text ,substrate-info))))

;; --- Config builder ---

(defun agent-shell--make-spirit-config (name &optional backend)
  "Build agent-config for spirit NAME on BACKEND.
BACKEND is a string (\"claude\", \"gemini\", \"codex\") or nil for project default.
Buffer name uses spirit#substrate notation; default substrate is elided."
  (let* ((resolved-backend (or backend (agent-shell--default-substrate)))
         (default-p (agent-shell--default-substrate-p resolved-backend))
         (buf-name (if default-p
                       name
                     (format "%s#%s" name resolved-backend)))
         (color (agent-shell--spirit-color name))
         (prompt (propertize (concat buf-name "> ")
                             'face `(:foreground ,color :weight bold))))
    (agent-shell-make-agent-config
     :identifier (intern buf-name)
     :buffer-name buf-name
     :mode-line-name buf-name
     :shell-prompt prompt
     :shell-prompt-regexp (concat (regexp-quote buf-name) "> ")
     :welcome-function (agent-shell--spirit-welcome buf-name resolved-backend)
     :client-maker (agent-shell--client-maker-for-backend resolved-backend))))

;; --- Entry point ---

(defun agent-shell-start-spirit (&optional name)
  "Start agent-shell with spirit identity.
Resolve NAME by: explicit argument → .guardian/identity → interactive prompt.
If none resolved, fall back to default config (mayadev).
With prefix arg, prompt for backend and force a new session."
  (interactive)
  (let* ((resolved (or name
                      (agent-shell--guardian-name)
                      (let ((input (read-string "Spirit (empty for default): ")))
                        (unless (string-empty-p input) input))))
         (backend (when current-prefix-arg
                    (completing-read "Backend: "
                                    (or (agent-shell--available-substrates)
                                        '("claude"))
                                    nil t nil nil "claude")))
         (config (if resolved
                     (agent-shell--make-spirit-config resolved backend)
                   agent-shell-default-config)))
    ;; One spirit, one presence: reuse existing session, C-u to force new.
    (let ((existing (seq-find
                     (lambda (buf)
                       (string-equal
                        (map-nested-elt
                         (buffer-local-value 'agent-shell--state buf)
                         '(:agent-config :buffer-name))
                        (map-elt config :buffer-name)))
                     (agent-shell-project-buffers))))
      (if (and existing (not current-prefix-arg))
          (agent-shell--display-buffer existing)
        (agent-shell--start :config config)))))

(provide 'spirit-session)
;;; spirit-session.el ends here
