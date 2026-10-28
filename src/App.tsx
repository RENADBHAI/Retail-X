import { FormEvent, ReactNode, useEffect, useState } from 'react'

type IconName =
  | 'spark'
  | 'message'
  | 'package'
  | 'users'
  | 'file'
  | 'chart'
  | 'clock'
  | 'paperclip'
  | 'send'
  | 'shield'
  | 'gavel'
  | 'user'
  | 'refresh'
  | 'search'
  | 'check'
  | 'arrow'
  | 'close'

const paths: Record<IconName, ReactNode> = {
  spark: <path d="M12 2.8c.5 4.4 2.8 6.7 7.2 7.2-4.4.5-6.7 2.8-7.2 7.2-.5-4.4-2.8-6.7-7.2-7.2 4.4-.5 6.7-2.8 7.2-7.2Z" />,
  message: <><path d="M20 11.5a7.5 7.5 0 0 1-8 7.5 8.8 8.8 0 0 1-3.5-.8L4 20l1.5-4A7.3 7.3 0 0 1 4 11.5 7.5 7.5 0 0 1 12 4a7.5 7.5 0 0 1 8 7.5Z" /><path d="M9 11.5h.01M12 11.5h.01M15 11.5h.01" /></>,
  package: <><path d="m4 7.5 8-4 8 4-8 4-8-4Z" /><path d="M4 7.5v9l8 4 8-4v-9M12 11.5v9" /></>,
  users: <><path d="M16 20v-1.5c0-2.2-1.8-4-4-4H7c-2.2 0-4 1.8-4 4V20" /><circle cx="9.5" cy="7.5" r="3.5" /><path d="M17 4.6a3.5 3.5 0 0 1 0 6.8M21 20v-1.5a4 4 0 0 0-2.5-3.7" /></>,
  file: <><path d="M6 3h8l4 4v14H6V3Z" /><path d="M14 3v5h4M9 12h6M9 16h6" /></>,
  chart: <><path d="M4 20V10M10 20V4M16 20v-7M22 20H2" /></>,
  clock: <><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></>,
  paperclip: <path d="m9 12.5 5.2-5.2a3 3 0 0 1 4.3 4.2l-6.8 6.8a5 5 0 1 1-7.1-7.1l7-7a2.8 2.8 0 0 1 4 4l-7 7a1 1 0 0 1-1.4-1.4l6.2-6.2" />,
  send: <><path d="m21 3-7.8 18-2.4-7.8L3 10.8 21 3Z" /><path d="m10.8 13.2 4-4" /></>,
  shield: <><path d="M12 3 20 6v5c0 5.1-3.3 8.2-8 10-4.7-1.8-8-4.9-8-10V6l8-3Z" /><path d="m8.5 12 2.2 2.2 4.8-5" /></>,
  gavel: <><path d="m14 5 5 5M12 7l5 5M3 21l8-8M5 16l3 3M3 21h8" /><path d="m15.5 3.5 5 5-2 2-5-5 2-2ZM9.5 9.5l5 5-2 2-5-5 2-2Z" /></>,
  user: <><circle cx="12" cy="7.5" r="3.5" /><path d="M5 21v-2a7 7 0 0 1 14 0v2" /></>,
  refresh: <><path d="M4 8V4h4M20 16v4h-4" /><path d="M5.5 5.5A9 9 0 0 1 20 10M18.5 18.5A9 9 0 0 1 4 14" /></>,
  search: <><circle cx="10.5" cy="10.5" r="6.5" /><path d="m16 16 5 5" /></>,
  check: <path d="m5 12.5 4.2 4.2L19 7" />,
  arrow: <><path d="M3 12h17M16 8l4 4-4 4" /></>,
  close: <path d="m6 6 12 12M18 6 6 18" />,
}

function Icon({ name, size = 20 }: { name: IconName; size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      {paths[name]}
    </svg>
  )
}

function Robot({ small = false }: { small?: boolean }) {
  return (
    <svg className={small ? 'robot robot--small' : 'robot'} viewBox="0 0 280 235" role="img" aria-label="Retail X AI assistant">
      <defs>
        <linearGradient id={`body-${small}`} x1="0" y1="0" x2="1" y2="1">
          <stop stopColor="#ffffff" />
          <stop offset=".64" stopColor="#eef7f5" />
          <stop offset="1" stopColor="#c9e4df" />
        </linearGradient>
        <linearGradient id={`glass-${small}`} x1="0" y1="0" x2="1" y2="1">
          <stop stopColor="#213b3c" />
          <stop offset="1" stopColor="#071a1c" />
        </linearGradient>
        <filter id={`shadow-${small}`} x="-30%" y="-30%" width="160%" height="180%">
          <feDropShadow dx="0" dy="14" stdDeviation="12" floodColor="#3b8275" floodOpacity=".18" />
        </filter>
        <filter id={`glow-${small}`}>
          <feGaussianBlur stdDeviation="3" result="blur" />
          <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
        </filter>
      </defs>
      {!small && <ellipse cx="138" cy="218" rx="72" ry="11" fill="#b7dcd5" opacity=".22" />}
      <g filter={`url(#shadow-${small})`}>
        <path d="M89 132c-15 6-22 21-18 39l8 31c3 11 13 18 24 16l10-2-2-68-22-16Z" fill={`url(#body-${small})`} stroke="#cce7e2" />
        <path d="M191 132c15 6 22 21 18 39l-8 31c-3 11-13 18-24 16l-10-2 2-68 22-16Z" fill={`url(#body-${small})`} stroke="#cce7e2" />
        <rect x="102" y="122" width="76" height="91" rx="35" fill={`url(#body-${small})`} stroke="#cce7e2" />
        <path d="M124 202h32" stroke="#96cbc2" strokeWidth="3" strokeLinecap="round" />
        <path d="M72 142c-17 3-24 17-20 29 3 10 12 15 21 13" fill="none" stroke="#eff9f7" strokeWidth="17" strokeLinecap="round" />
        <circle cx="51" cy="170" r="11" fill={`url(#glass-${small})`} />
        <path d="M207 141c18-2 28-14 28-27" fill="none" stroke="#eff9f7" strokeWidth="17" strokeLinecap="round" />
        <circle cx="235" cy="107" r="11" fill={`url(#glass-${small})`} />
        <path d="m136 149 5 11 11 5-11 5-5 11-5-11-11-5 11-5 5-11Z" fill="#20b99a" opacity=".86" />
        <rect x="67" y="28" width="143" height="115" rx="56" transform="rotate(-4 67 28)" fill={`url(#body-${small})`} stroke="#cce7e2" />
        <rect x="79" y="42" width="120" height="86" rx="42" transform="rotate(-4 79 42)" fill={`url(#glass-${small})`} />
        <path d="M104 87c3-13 17-16 24-5M160 78c7-10 20-6 21 7" fill="none" stroke="#76ffe2" strokeWidth="5" strokeLinecap="round" filter={`url(#glow-${small})`} />
        <path d="M125 104c10 8 22 7 30-3" fill="none" stroke="#76ffe2" strokeWidth="4" strokeLinecap="round" filter={`url(#glow-${small})`} />
        <path d="M91 46c13-10 29-14 46-13" fill="none" stroke="white" strokeWidth="4" strokeLinecap="round" opacity=".75" />
        <circle cx="71" cy="88" r="8" fill="#28c8aa" />
        <path d="M203 83c9 2 14 10 13 19" fill="none" stroke="#29c6aa" strokeWidth="5" strokeLinecap="round" />
      </g>
    </svg>
  )
}

const nav = [
  ['New Request', 'message'],
  ['Orders', 'package'],
  ['Customers', 'users'],
  ['Policies', 'file'],
  ['Analytics', 'chart'],
  ['History', 'clock'],
] as const

const quickActions = [
  { label: 'Check order status', icon: 'package', tone: 'mint' },
  { label: 'Cancel an order', icon: 'refresh', tone: 'lavender' },
  { label: 'Return policy', icon: 'file', tone: 'amber' },
  { label: 'Find customer', icon: 'search', tone: 'blue' },
] as const


type WorkflowStep = {
  title: string
  icon: IconName
  tone: 'mint' | 'lavender' | 'amber' | 'blue' | 'coral'
  text: string
  state: 'done' | 'active' | 'waiting' | 'blocked'
}

type OrderView = {
  order_id: string
  status: string
  items: Array<{ name: string; quantity: number; price: number }>
  total: number
}

type AgentResponse = {
  answer: string
  workflow: WorkflowStep[]
  order: OrderView | null
  requires_approval: boolean
  action_id: string | null
  approval_summary?: string | null
}

const initialWorkflow: WorkflowStep[] = [
  { title: 'Identity Verification', icon: 'shield', tone: 'mint', text: 'Waiting for a customer request.', state: 'waiting' },
  { title: 'Retrieve Order', icon: 'package', tone: 'lavender', text: 'Order data will appear here.', state: 'waiting' },
  { title: 'Policy Check', icon: 'file', tone: 'amber', text: 'Retail policy will be checked when needed.', state: 'waiting' },
  { title: 'Decision', icon: 'gavel', tone: 'blue', text: 'No decision yet.', state: 'waiting' },
  { title: 'Human Approval', icon: 'user', tone: 'coral', text: 'Write actions require explicit approval.', state: 'waiting' },
]

const API_BASE = ''

function App() {
  const [input, setInput] = useState('')
  const [request, setRequest] = useState('Loading a real demo case…')
  const [workflow, setWorkflow] = useState<WorkflowStep[]>(initialWorkflow)
  const [isRunning, setIsRunning] = useState(false)
  const [approvalOpen, setApprovalOpen] = useState(false)
  const [decision, setDecision] = useState<'approved' | 'rejected' | null>(null)
  const [answer, setAnswer] = useState('Ask me about a real order, policy, or cancellation.')
  const [order, setOrder] = useState<OrderView | null>(null)
  const [actionId, setActionId] = useState<string | null>(null)
  const [approvalSummary, setApprovalSummary] = useState<string>('No write action pending.')
  const [error, setError] = useState<string | null>(null)
  const [approvalBusy, setApprovalBusy] = useState(false)

  useEffect(() => {
    let cancelled = false

    async function loadDemo() {
      try {
        const response = await fetch(`${API_BASE}/api/demo-case`)
        if (!response.ok) throw new Error('Backend is not reachable.')
        const data = await response.json()
        if (!cancelled) {
          setRequest(data.prompt)
          setInput(data.prompt)
          setAnswer('Demo case loaded. Press Send to run the real Retail X workflow.')
        }
      } catch {
        if (!cancelled) {
          setRequest('Connect the Retail X backend, then send a request.')
          setAnswer('Backend offline — start server.py on port 8000.')
        }
      }
    }

    loadDemo()
    return () => { cancelled = true }
  }, [])

  const runRequest = async (nextRequest: string) => {
    if (!nextRequest.trim() || isRunning) return

    setRequest(nextRequest)
    setInput('')
    setDecision(null)
    setApprovalOpen(false)
    setError(null)
    setIsRunning(true)
    setAnswer('Retail X is running the workflow…')
    setWorkflow(initialWorkflow.map((step, i) => ({
      ...step,
      state: i === 0 ? 'active' : 'waiting'
    })))

    try {
      const response = await fetch(`${API_BASE}/api/agent`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: nextRequest })
      })

      const data: AgentResponse & { detail?: string } = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'The agent request failed.')
      }

      setWorkflow(data.workflow)
      setAnswer(data.answer)
      setOrder(data.order)
      setActionId(data.action_id)
      setApprovalSummary(data.approval_summary || 'No write action pending.')

      if (data.requires_approval && data.action_id) {
        setApprovalOpen(true)
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error'
      setError(message)
      setAnswer('I could not complete the request because the backend returned an error.')
    } finally {
      setIsRunning(false)
    }
  }

  const submit = (event: FormEvent) => {
    event.preventDefault()
    runRequest(input)
  }

  const approveAction = async (approve: boolean) => {
    if (!actionId || approvalBusy) return

    setApprovalBusy(true)
    setError(null)

    try {
      const response = await fetch(`${API_BASE}/api/approval`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action_id: actionId,
          decision: approve ? 'approve' : 'reject'
        })
      })

      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'Approval failed.')

      setDecision(approve ? 'approved' : 'rejected')
      setApprovalOpen(false)
      setAnswer(data.message)
      setActionId(null)
      setApprovalSummary(approve ? 'Approved and completed.' : 'Rejected. No write was executed.')

      setWorkflow((steps) => steps.map((step, index) => (
        index === 4
          ? {
              ...step,
              state: 'done',
              text: approve
                ? 'Human approved the write action. The working order was updated.'
                : 'Human rejected the write action. No change was made.'
            }
          : step
      )))

      if (data.order) setOrder(data.order)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error'
      setError(message)
    } finally {
      setApprovalBusy(false)
    }
  }

  const currentMessage = isRunning ? 'Running the Retail X agent…' : answer

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand__name">Retail X</div>
          <div className="brand__tagline">Retail Operations AI Agent</div>
        </div>
        <nav className="nav" aria-label="Main navigation">
          {nav.map(([label, icon], index) => (
            <button className={`nav__item ${index === 0 ? 'nav__item--active' : ''}`} key={label} type="button">
              <Icon name={icon} />
              <span>{label}</span>
            </button>
          ))}
        </nav>
        <div className="sidebar__status">
          <span className="status-dot" />
          <div><strong>Agent online</strong><span>API-connected workflow</span></div>
        </div>
      </aside>

      <main className="workspace">
        <header className="topbar">
          <div>
            <span className="eyebrow"><Icon name="spark" size={14} /> Intelligent operations</span>
            <h1>How can I help?</h1>
          </div>
          <button className="profile-button" type="button" aria-label="Open user profile"><Icon name="user" size={19} /></button>
        </header>

        <section className="agent-stage" aria-label="Retail X assistant">
          <div className="robot-wrap"><Robot /></div>
          <div className={`speech ${isRunning ? 'speech--active' : ''}`}>
            <div className="speech__label"><span className="live-dot" /> RETAIL X</div>
            <div className="speech__hello">{isRunning ? 'Working on it' : 'Hello! 👋'}</div>
            <div className="speech__main">{currentMessage}</div>
            <div className="speech__secondary">
              Identity, order ownership, policy and write approvals are enforced by the backend harness.
            </div>
            {isRunning && <div className="thinking"><i /><i /><i /></div>}
          </div>
        </section>

        <div className="quick-actions" aria-label="Quick actions">
          {quickActions.map((action) => (
            <button
              className={`quick-action quick-action--${action.tone}`}
              type="button"
              key={action.label}
              onClick={() => setInput(action.label)}
            >
              <Icon name={action.icon} size={17} />
              {action.label}
            </button>
          ))}
        </div>

        <form className="request-box" onSubmit={submit}>
          <Icon name="paperclip" size={21} />
          <input
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Example: My email is ... Check order #... and cancel it."
            aria-label="Request"
          />
          <button type="submit" aria-label="Send request" disabled={isRunning}>
            <Icon name="send" size={19} />
          </button>
        </form>

        {error && <div className="api-error">Backend error: {error}</div>}

        <section className="conversation" aria-label="Conversation">
          <div className="message-row message-row--user">
            <div className="message message--user">{request}</div>
            <div className="avatar avatar--user"><Icon name="user" size={18} /></div>
          </div>
          <div className="message-row message-row--agent">
            <div className="avatar avatar--robot"><Robot small /></div>
            <div className="message message--agent">
              <span className="message__name">Retail X</span>
              {answer}
            </div>
          </div>
        </section>

        <section className="workflow-section" aria-labelledby="workflow-title">
          <div className="section-heading">
            <div>
              <span className="eyebrow">LIVE AGENT WORKFLOW</span>
              <h2 id="workflow-title">From request to safe action</h2>
            </div>
            <span className="workflow-status">
              <span className={isRunning ? 'pulse' : ''} />
              {isRunning ? 'Executing' : 'Analysis complete'}
            </span>
          </div>

          <div className="workflow">
            {workflow.map((step, index) => {
              const complete = step.state === 'done'
              const active = step.state === 'active'
              return (
                <div className="workflow-pair" key={step.title}>
                  <article className={`workflow-card workflow-card--${step.tone} ${complete ? 'is-complete' : ''} ${active ? 'is-active' : ''}`}>
                    <div className="workflow-card__top">
                      <span className="workflow-card__icon"><Icon name={step.icon} size={19} /></span>
                      <span className={`step-state ${complete ? 'step-state--done' : active ? 'step-state--active' : ''}`}>
                        {complete ? <Icon name="check" size={12} /> : index + 1}
                      </span>
                    </div>
                    <h3>{step.title}</h3>
                    <p>{step.text}</p>
                    {index === 4 && actionId && (
                      <button className="approval-button" type="button" onClick={() => setApprovalOpen(true)}>
                        {decision === 'approved' ? 'Approved' : decision === 'rejected' ? 'Rejected' : 'Request Approval'}
                      </button>
                    )}
                  </article>
                  {index < workflow.length - 1 && (
                    <div className={`connector ${complete ? 'connector--done' : ''}`}>
                      <Icon name="arrow" size={18} />
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </section>
      </main>

      <aside className="order-panel">
        <div className="order-panel__glow" />
        <div className="order-header">
          <div>
            <span className="eyebrow">SELECTED ORDER</span>
            <h2>{order ? `Order ${order.order_id}` : 'No order selected'}</h2>
          </div>
          <span className="badge">{order?.status || 'Waiting'}</span>
        </div>

        <div className="timeline">
          {['Order Placed', 'Processing', 'Shipped', 'Delivered'].map((label, index) => {
            const status = (order?.status || '').toLowerCase()
            const currentIndex =
              status === 'pending' ? 0 :
              status === 'processed' ? 1 :
              status === 'delivered' ? 3 :
              status === 'cancelled' ? 1 : 0
            const state = order
              ? index < currentIndex ? 'done' : index === currentIndex ? 'current' : 'future'
              : 'future'

            return (
              <div className={`timeline__item timeline__item--${state}`} key={label}>
                <span className="timeline__marker">{state === 'done' && <Icon name="check" size={11} />}</span>
                <div>
                  <strong>{label}</strong>
                  <span>{order ? (state === 'future' ? 'Pending' : order.status) : '—'}</span>
                </div>
              </div>
            )
          })}
        </div>

        <div className="divider" />
        <div className="items-title">
          <h3>Items <span>{order?.items.length || 0}</span></h3>
          <Icon name="arrow" size={16} />
        </div>

        {order?.items.length ? (
          order.items.map((item, index) => (
            <div className="product" key={`${item.name}-${index}`}>
              <div className={`product__image ${index % 2 === 0 ? 'headphones' : 'mouse'}`}>
                <i /><i />
              </div>
              <div>
                <strong>{item.name}</strong>
                <span>SAR {item.price.toFixed(2)} × {item.quantity}</span>
              </div>
            </div>
          ))
        ) : (
          <div className="empty-order">Run a request to load a real τ²-Bench order.</div>
        )}

        <div className="divider" />
        <div className="price-row price-row--total">
          <span>Total</span>
          <strong>SAR {(order?.total || 0).toFixed(2)}</strong>
        </div>

        <div className="secure-note">
          <Icon name="shield" size={16} />
          <span>Protected by Retail X ownership and approval policy</span>
        </div>
      </aside>

      {approvalOpen && actionId && (
        <div className="modal-backdrop" role="presentation" onMouseDown={() => setApprovalOpen(false)}>
          <div
            className="approval-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="approval-title"
            onMouseDown={(event) => event.stopPropagation()}
          >
            <button className="modal-close" type="button" onClick={() => setApprovalOpen(false)} aria-label="Close approval dialog">
              <Icon name="close" size={18} />
            </button>
            <div className="approval-modal__icon"><Icon name="shield" size={25} /></div>
            <span className="eyebrow">HUMAN IN THE LOOP</span>
            <h2 id="approval-title">Approval Required</h2>
            <p>{approvalSummary}</p>

            <div className="approval-checks">
              {[
                'Customer identity verified',
                'Order ownership verified',
                'Retail policy checked',
                'Write action eligible'
              ].map((item) => (
                <div key={item}>
                  <span><Icon name="check" size={13} /></span>
                  {item}
                </div>
              ))}
            </div>

            <div className="modal-actions">
              <button className="reject-button" type="button" disabled={approvalBusy} onClick={() => approveAction(false)}>Reject</button>
              <button className="approve-button" type="button" disabled={approvalBusy} onClick={() => approveAction(true)}>
                <Icon name="check" size={17} />
                Approve cancellation
              </button>
            </div>

            <div className="modal-footnote">
              <Icon name="shield" size={14} />
              No database write occurs without this approval.
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App