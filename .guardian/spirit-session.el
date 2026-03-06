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

(defun agent-shell--format-spirit-banner (name identity-text)
  "Format a welcome banner for spirit NAME with IDENTITY-TEXT."
  (concat "\n"
          (if identity-text
              (concat "  ┌─ " name " ─────────────────────────\n"
                      (mapconcat (lambda (line) (concat "  │ " line))
                                 (split-string identity-text "\n")
                                 "\n")
                      "\n  └──────────────────────────────────\n")
            (format "  Spirit: %s (no identity.yaml found)\n" name))))

(defun agent-shell--spirit-welcome (name)
  "Return a welcome function for spirit NAME.
Captures identity text eagerly (at config-build time) so it survives
agent-shell rebinding `default-directory' to the project cwd."
  (let ((banner (agent-shell--format-spirit-banner
                 name (agent-shell--spirit-identity-text))))
    `(lambda (_config) ,banner)))

(defun agent-shell--make-spirit-config (name)
  "Build agent-config for spirit NAME."
  (agent-shell-make-agent-config
   :identifier (intern name)
   :buffer-name name
   :mode-line-name name
   :shell-prompt (concat name "> ")
   :shell-prompt-regexp (concat (regexp-quote name) "> ")
   :welcome-function (agent-shell--spirit-welcome name)
   :client-maker (lambda (buffer)
                   (agent-shell-anthropic-make-claude-client :buffer buffer))))

(defun agent-shell-start-spirit (&optional name)
  "Start agent-shell with spirit identity.
Resolve NAME by: explicit argument → .guardian/identity → interactive prompt.
If none resolved, fall back to default config (mayadev)."
  (interactive)
  (let* ((resolved (or name
                      (agent-shell--guardian-name)
                      (let ((input (read-string "Spirit (empty for default): ")))
                        (unless (string-empty-p input) input))))
         (config (if resolved
                     (agent-shell--make-spirit-config resolved)
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
