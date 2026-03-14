# Model-Market

Build financial models for small enterprise — options strategies,
demand surfaces, hedging instruments, margin analysis.

## Purpose

Most financial modelling assumes institutional actors with market
access, real-time data feeds, and quantitative literacy. This power
adapts the same instruments for contexts where none of those hold:
a shopkeeper in Barnala who hedges seasonally by gut feel, a weaver
in Kullu who prices shawls by cost-plus with no demand curve.

The spirit reads market structure and produces models that can be
explained in a conversation — not just computed, but understood.
The model must survive translation to a WhatsApp message.

## When to Use

- A commission needs to understand the economics of its domain
  (apparel margins, seasonal inventory, fabric sourcing)
- An options or hedging strategy needs to be modelled for a specific
  retail context (forward buying, put-like inventory insurance)
- Demand forecasting is needed (time series, seasonal decomposition,
  volatility estimation)
- A pricing surface needs to be constructed from sparse data
  (small-town retail has no Bloomberg terminal)
- Supply chain economics need analysis (producer margins, middleman
  extraction, disintermediation opportunity)

## Procedure

### 1. Understand the domain

Before modelling, survey:
- What does the business actually buy and sell?
- What are the seasonal patterns? (Eid stock, wedding season, monsoon)
- What data exists? (Tally exports, handwritten ledgers, WhatsApp messages)
- What instruments does the shopkeeper already use intuitively?
  (Forward buying, bulk discounts, credit terms — these are informal derivatives)
- Who are the intermediaries and what do they extract?

### 2. Choose the modelling frame

Match the financial instrument to the business reality:

| Business reality | Financial analogue | Model |
|------------------|--------------------|-------|
| "Buy extra stock before Eid" | Call option on inventory | Seasonal demand model + optimal order quantity |
| "Return unsold stock to supplier" | Put option | Return policy as embedded option — value it |
| "Supplier offers 60-day credit" | Trade credit as financing | Implicit interest rate, compare to alternatives |
| "Price drops after season" | Inventory depreciation | Markdown optimisation (when to discount, how much) |
| "Fabric price is unpredictable" | Commodity volatility | Historical volatility + simple hedging strategy |
| "Customer buys on credit" | Accounts receivable | Credit risk model + collection probability |

### 3. Build the model

Produce a computational artifact (Python, typically):
- Use standard libraries: `numpy`, `scipy`, `pandas`
- For options: implement or adapt Black-Scholes, binomial trees,
  or Monte Carlo as appropriate
- For time series: seasonal decomposition, ARIMA, or Prophet
- For optimisation: `scipy.optimize` or linear programming
- Document assumptions explicitly — small-enterprise data is sparse
  and assumptions carry most of the weight

### 4. Validate against reality

- Backtest if historical data exists
- Sensitivity analysis on key assumptions
- Sanity-check with domain knowledge (does the model agree with
  what experienced shopkeepers already know intuitively?)
- Translate the result into plain language — if you can't explain
  the model's recommendation in two sentences, the model is wrong
  for this context

### 5. Deliver

- Code goes into the relevant commission's repo
- Results summarised in a WP or relay message
- If the model reveals something surprising, write it up —
  the organisation learns from what sarraf sees

## Key Principles

- **The shopkeeper is the oracle.** Formal data is sparse. The
  shopkeeper's twenty years of gut feel *is* the dataset. Model
  it, don't replace it.
- **Instruments exist in disguise.** A return policy is a put option.
  A bulk discount is a volume-triggered forward. Name the instrument
  but don't require the shopkeeper to learn the name.
- **Explain or discard.** A model that can't be explained to the
  commission's guardian spirit in two paragraphs is too complex for
  the context. Simplify until it survives translation.
- **Sparse data demands strong priors.** When you have 12 months of
  Tally data and no market feed, Bayesian methods with informative
  priors outperform frequentist approaches. State your priors.
- **The model serves the commission.** Sarraf doesn't trade. She
  reads the market and reports what she sees. The commission decides
  what to do with it.
