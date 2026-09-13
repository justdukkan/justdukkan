# Article content for /insights. Edit here, then run tools/build_insights.py.

ARTICLES = [
{
 'slug': 'hub-and-spoke-agent-architecture',
 'short': 'Hub-and-spoke agent architecture',
 'kicker': 'Agentic systems',
 'title': 'Hub-and-spoke agent architecture: how to build multi-agent systems that stay explainable',
 'desc': 'A hub-and-spoke architecture puts one orchestrator in charge of planning, routing and verification, and gives every specialist agent, tool and human reviewer a bounded job. Here is how the pattern works, when to use it, and the design rules that keep it safe in production.',
 'read': 8,
 'about': ['Multi-agent systems', 'AI orchestration', 'Agentic architecture'],
 'keywords': ['hub-and-spoke architecture', 'multi-agent system', 'orchestrator agent', 'agentic workflow', 'MCP', 'human in the loop'],
 'body': '''
<h2>What hub-and-spoke means for AI agents</h2>
<p>A <strong>hub-and-spoke agent architecture</strong> is a way of organising a system of AI agents so that exactly one component, the <strong>orchestrator</strong> (the hub), owns the plan, and every other component, the <strong>spokes</strong>, does one bounded job on request. Spokes are specialist agents, tool servers (for example MCP servers that wrap an ERP, a helpdesk or a document store), data sources, and human reviewers.</p>
<p>The hub never touches company systems directly and the spokes never talk to each other. All communication travels through the hub over <strong>typed tool contracts</strong>: a named operation, a schema for its input and output, an explicit permission, and a log entry. The result is a system where you can always answer three questions: what was the plan, who did each step, and what did each step change.</p>

<h2>Why not let agents talk to each other?</h2>
<p>Fully connected "swarm" designs, where any agent can call any other, are quick to demo and slow to operate. They fail in predictable ways:</p>
<ul>
  <li><strong>No single place to reason about the plan.</strong> When a run goes wrong you reconstruct it from six agents' logs.</li>
  <li><strong>Permissions leak.</strong> If a summarising agent can call the agent that posts invoices, it effectively has posting rights.</li>
  <li><strong>Cost is unbounded.</strong> Agents that can call each other can loop; every loop is a bill.</li>
  <li><strong>Testing is combinatorial.</strong> Each new agent multiplies the paths you have to evaluate.</li>
</ul>
<p>Hub-and-spoke trades a little flexibility for a lot of control. The hub is the only component with a global view, so it is the only one that needs global reasoning ability. Spokes can be small, cheap and specialised.</p>

<h2>The five roles in a hub-and-spoke system</h2>
<table>
  <tr><th>Role</th><th>Responsibility</th><th>Typical implementation</th></tr>
  <tr><td>Orchestrator (hub)</td><td>Turns a request into a plan, routes steps to spokes, verifies results, decides when to stop or ask a human</td><td>A capable model (e.g. Claude Opus or Sonnet class) with a small, fixed tool set: <code>delegate</code>, <code>call_tool</code>, <code>request_approval</code>, <code>finish</code></td></tr>
  <tr><td>Specialist agents</td><td>One domain each: documents, finance rules, support replies, compliance checks</td><td>Smaller or cheaper models with a narrow system prompt and only the tools that domain needs</td></tr>
  <tr><td>Tool servers</td><td>Deterministic access to systems: read a PDF, match a purchase order, create a ticket</td><td>MCP servers or internal APIs with JSON schemas and scoped credentials</td></tr>
  <tr><td>Knowledge</td><td>Retrieval over company documents and data so answers are grounded, not remembered</td><td>Indexed document store with chunking, metadata filters and citations</td></tr>
  <tr><td>Human review</td><td>Approve, reject or correct at defined checkpoints</td><td>A queue in the tool your team already uses (Slack, email, helpdesk) with a typed decision returned to the hub</td></tr>
</table>

<h2>How a run flows</h2>
<ol>
  <li><strong>Intake.</strong> A request arrives: an email, a scheduled trigger, a form, a webhook.</li>
  <li><strong>Plan.</strong> The hub writes a short plan: which spokes, in what order, which steps need approval. The plan is stored before execution starts, so it can be audited even if the run fails.</li>
  <li><strong>Delegate.</strong> Each step is a tool call with a schema-validated input. Specialist agents return structured results, not prose.</li>
  <li><strong>Verify.</strong> The hub checks each result against the plan: did the invoice match a purchase order, is the confidence above the threshold, does the total cross an approval limit.</li>
  <li><strong>Checkpoint.</strong> Steps with real-world consequences (posting, sending, creating, paying) pause for a human decision when policy says so. The decision is itself a typed input.</li>
  <li><strong>Finish.</strong> The hub produces a summary, the run's cost and duration, and a complete log of every tool call.</li>
</ol>

<h2>Design rules that keep it safe</h2>
<h3>1. Every edge is a contract</h3>
<p>No free-text calls between components. Each tool has a name, an input schema, an output schema and a documented side effect. If a spoke cannot express what it needs in the schema, the schema is wrong, not the rule.</p>
<h3>2. Permissions live on the tool, not the agent</h3>
<p>The finance agent does not "have ERP access"; it has access to <code>erp.match_po</code> (read) and, only after approval, the hub has access to <code>erp.post_invoice</code> (write). Scoping credentials per tool makes the blast radius of any single prompt-injection or model error small and visible.</p>
<h3>3. Reads are free, writes wait</h3>
<p>Default policy: agents can read and compute without asking; any write to a system of record goes through a policy check and, above a risk threshold, a human. The threshold is a business rule (amount, customer tier, novelty), not a model judgement.</p>
<h3>4. Ground answers in retrieval</h3>
<p>Spokes that answer questions must cite the document or record they used. If retrieval returns nothing, the correct output is "not found", never a plausible guess.</p>
<h3>5. Budget every run</h3>
<p>The hub carries a token and time budget. Exceeding it is a terminal state that returns to a human, not a retry.</p>
<h3>6. Evaluate before and after</h3>
<p>Keep a test set of real requests with known correct outcomes. Run it before every prompt, model or tool change. A system you cannot re-evaluate is a system you cannot change.</p>

<h2>When to use it, and when not to</h2>
<p>Hub-and-spoke is the right default when a process touches more than one system, has steps with different risk levels, or must be explained to an auditor, a customer or a regulator. That covers most back-office automation: invoice intake, vendor onboarding, support triage, contract review, order exceptions.</p>
<p>It is overkill for a single-step task ("summarise this document", "classify this email"). Those are one spoke with no hub; build them as a plain tool and keep the option to plug them into a hub later.</p>

<h2>Adding a capability is adding a spoke</h2>
<p>The practical payoff shows up months in. When the business asks for a new step, say sanctions screening during vendor onboarding, you add one tool server and one line to the hub's policy. The plan format, the approval flow, the logging and the evaluation harness are unchanged. That is what "easy to extend" should mean for an AI system: new work without new risk.</p>
''',
 'faq': [
  ('Is hub-and-spoke the same as an "agent supervisor" pattern?', 'They are close relatives. Supervisor patterns describe the hub; hub-and-spoke additionally fixes the rules for the spokes: no spoke-to-spoke calls, typed contracts on every edge, permissions attached to tools rather than agents, and human checkpoints as first-class steps.'),
  ('Does the orchestrator need the most expensive model?', 'Usually the hub benefits from a stronger model because it does the planning and verification, while spokes can run on smaller, cheaper models. Model routing is a design decision: each step uses the cheapest model that passes the evaluation set.'),
  ('How does MCP fit into hub-and-spoke?', 'MCP (Model Context Protocol) servers are the natural implementation of tool spokes. Each server exposes typed tools with schemas, which is exactly the contract the hub needs, and credentials can be scoped per server.'),
 ],
},
{
 'slug': 'mcp-server-and-tool-design',
 'short': 'MCP server & tool design',
 'kicker': 'MCP & tools',
 'title': 'Designing MCP servers and tools that agents can use safely',
 'desc': 'MCP gives agents a standard way to call tools, but a badly designed tool is still a badly designed tool. These are the rules we use for tool contracts, permissions, error handling and logging when we build Model Context Protocol servers for company systems.',
 'read': 7,
 'about': ['Model Context Protocol', 'Tool design', 'AI agent security'],
 'keywords': ['MCP server', 'Model Context Protocol', 'tool design', 'agent tools', 'tool contract', 'permissions', 'prompt injection'],
 'body': '''
<h2>What an MCP server is, in one paragraph</h2>
<p>The <strong>Model Context Protocol (MCP)</strong> is an open standard that lets an AI application discover and call tools, read resources and use prompts exposed by a server, over a common wire format. An <strong>MCP server</strong> wraps something you already have, an ERP, a helpdesk, a document store, an internal API, and presents it to agents as a list of named tools with JSON schemas. The agent side (Claude, an orchestrator you built, an IDE) is the client. The protocol solves the plumbing; it does not decide what the tools should be. That is the design work.</p>

<h2>Rule 1: model the business operation, not the API</h2>
<p>The most common mistake is to auto-generate a tool per REST endpoint. Agents then get <code>GET /invoices</code>, <code>PATCH /invoices/{id}</code> and forty siblings, and have to reconstruct business meaning from HTTP verbs. Instead, expose the operations a competent employee would name:</p>
<pre><code># reads: no side effect
erp.match_po(invoice_ref, vendor, total) → {status, po_number, variance}
helpdesk.fetch_new(since)                → [ticket]

# writes: reversible, not visible to the customer
helpdesk.draft_reply(ticket_id, body)    → {draft_id}

# writes: irreversible or customer-visible, need approval
erp.post_invoice(invoice_id, po_number)  → {posted_id}
helpdesk.send_reply(draft_id)            → {sent_at}</code></pre>
<p>Fewer, meaningful tools produce better plans, fewer wrong calls and a permission model humans can read.</p>

<h2>Rule 2: separate reads, drafts and sends</h2>
<p>Split every side-effecting operation into stages that map to risk:</p>
<ul>
  <li><strong>Read</strong>: no side effect. Agents may call freely within a budget.</li>
  <li><strong>Draft / stage</strong>: creates something reversible and invisible to the outside world (a draft reply, a pending journal entry).</li>
  <li><strong>Commit / send</strong>: irreversible or externally visible. Gated by policy and, above a threshold, by a human.</li>
</ul>
<p>This lets the orchestrator do all the work up to the last step, show a human exactly what will happen, and then commit with one call. It also makes evaluation cheap: you can run the whole pipeline in tests without ever hitting a commit tool.</p>

<h2>Rule 3: schemas are the contract, so make them strict</h2>
<ul>
  <li>Use enums for anything that has a fixed set of values (status, currency, category). Free text invites hallucinated values.</li>
  <li>Require identifiers, not names, for anything that is looked up (<code>vendor_id</code>, not <code>vendor_name</code>). Provide a separate search tool that returns identifiers.</li>
  <li>Bound every list and string (<code>maxItems</code>, <code>maxLength</code>); bound every numeric field the business bounds.</li>
  <li>Return structured results with a stable shape. Never return a blob of prose for the model to parse.</li>
  <li>Write the tool description for the model: what it does, when to use it, when not to, and what it costs. This text is part of the prompt.</li>
</ul>

<h2>Rule 4: permissions belong to the server and the credential</h2>
<p>An MCP server should run with the narrowest credential that its tools need, and one server should not mix read-only and commit tools unless they share a risk level. In practice we deploy separate servers (or separate credentials on one server) for <em>read</em> and <em>commit</em>, and the orchestrator is the only client that holds the commit connection. Specialist agents get the read server. Whatever a prompt injection inside a document manages to convince a specialist agent to do, it cannot post an invoice.</p>

<h2>Rule 5: treat every tool result as untrusted input</h2>
<p>Tool results carry data from outside: PDF contents, email bodies, ticket text, web pages. That data can contain instructions aimed at the model. Defences that work in practice:</p>
<ul>
  <li>Wrap external content in clearly delimited fields and tell the model it is data, not instruction.</li>
  <li>Keep commit tools out of reach of any agent that reads external content.</li>
  <li>Have the orchestrator verify results against the plan rather than accept them.</li>
  <li>Log the raw input of every tool call so an incident can be traced to its source document.</li>
</ul>

<h2>Rule 6: errors are part of the contract</h2>
<p>Return typed errors the model can act on: <code>not_found</code>, <code>ambiguous(candidates=[...])</code>, <code>permission_denied</code>, <code>rate_limited(retry_after)</code>, <code>validation_failed(field, reason)</code>. A generic 500 with a stack trace teaches the model nothing and usually triggers a retry loop. Decide per error whether the correct behaviour is retry, ask the user, or stop.</p>

<h2>Rule 7: log for the auditor, not the developer</h2>
<p>Each call record should include: run id, calling agent, tool name, input (redacted where required), output summary, duration, cost, and the approval reference for commit tools. From that log you should be able to answer "who changed this record and why" without opening a model transcript.</p>

<h2>A checklist before an MCP server goes to production</h2>
<ol>
  <li>Every tool has a one-sentence purpose a business owner would recognise.</li>
  <li>Reads, drafts and commits are distinct tools with distinct credentials.</li>
  <li>All inputs are schema-validated server-side; enums and identifiers used wherever possible.</li>
  <li>Descriptions say when not to use the tool.</li>
  <li>Typed errors; no retries on non-retryable errors.</li>
  <li>Rate limits and per-run budgets enforced by the server, not the prompt.</li>
  <li>Structured audit log with approval references.</li>
  <li>A replayable test set of calls with expected outputs, run on every change.</li>
</ol>
''',
 'faq': [
  ('Can I expose my whole API through MCP automatically?', 'You can, and it is a fast way to prototype, but for production we model business operations rather than endpoints. Fewer, meaningful, schema-strict tools give agents better plans and give you a permission model people can review.'),
  ('How many tools should one MCP server expose?', 'As few as the domain needs; a dozen is common, more than thirty is a signal the server covers too many risk levels or too many domains and should be split.'),
  ('Does MCP handle authentication and permissions?', 'MCP standardises how tools are described and called. Which credential a server uses, and which client may reach which server, is your architecture. We scope credentials per server and keep commit tools reachable only by the orchestrator.'),
 ],
},
{
 'slug': 'process-automation-architecture',
 'short': 'Process automation architecture',
 'kicker': 'Process automation',
 'title': 'From manual process to automated flow: an architecture playbook',
 'desc': 'Most automation projects fail before the first model call, in the mapping and the boundaries. This is the sequence we use to take a process like invoice intake or support triage from hours of manual work to a running system with humans only where they matter.',
 'read': 9,
 'about': ['Business process automation', 'AI automation', 'Solution architecture'],
 'keywords': ['process automation', 'AI automation', 'invoice processing automation', 'support triage automation', 'human in the loop', 'cost model'],
 'body': '''
<h2>Start from a process, not from a model</h2>
<p>The question "where can we use AI?" produces demos. The question "which process costs us the most hours and why?" produces systems. We begin every engagement with one process, chosen for three properties: it is frequent, it is mostly rule-following with a few judgement calls, and its cost is visible to the business. Invoice intake, support triage, vendor onboarding, order exceptions and contract intake all qualify.</p>

<h2>Step 1: map the process as it actually runs</h2>
<p>Sit with the people who do the work and record the real flow, including the workarounds. For each step capture:</p>
<ul>
  <li><strong>Input</strong>: where it comes from (email, portal, ERP screen, spreadsheet) and in what format.</li>
  <li><strong>Decision</strong>: what the person checks and what rule they apply, including the unwritten ones.</li>
  <li><strong>Output</strong>: what changes in which system.</li>
  <li><strong>Exceptions</strong>: what happens when something does not fit, and how often.</li>
  <li><strong>Time and volume</strong>: minutes per item, items per week, and who does it.</li>
</ul>
<p>The map usually shows that 70–90% of items follow a handful of paths and the remainder consume most of the time. That split is the design.</p>

<h2>Step 2: draw the boundary between automation and judgement</h2>
<p>Classify each decision in the map:</p>
<table>
  <tr><th>Decision type</th><th>Handled by</th><th>Example</th></tr>
  <tr><td>Deterministic rule</td><td>Code, not a model</td><td>Invoice total equals PO total within tolerance</td></tr>
  <tr><td>Extraction / classification</td><td>Model with structured output, verified by rules</td><td>Read vendor, total, date and PO reference from a PDF</td></tr>
  <tr><td>Bounded judgement</td><td>Model with retrieval and a confidence threshold</td><td>Choose the best knowledge-base article for a ticket</td></tr>
  <tr><td>Consequential judgement</td><td>Human, presented with the model's preparation</td><td>Approve a payment above a limit; reply to an angry enterprise customer</td></tr>
</table>
<p>The rule is simple: models prepare, rules verify, humans decide where consequences are real. Automating the last column is where projects lose trust.</p>

<h2>Step 3: design the target architecture before building</h2>
<p>Write it down; a two-page document is enough. It should contain:</p>
<ol>
  <li><strong>Trigger and intake</strong>: how items enter (mailbox polling, webhook, schedule) and how duplicates are handled.</li>
  <li><strong>Orchestration</strong>: the plan for a normal item and for each known exception path. We use a <a href="/insights/hub-and-spoke-agent-architecture/">hub-and-spoke</a> structure so every step is a typed tool call.</li>
  <li><strong>Tools</strong>: the systems touched and the exact operations, split into read, draft and commit (see <a href="/insights/mcp-server-and-tool-design/">MCP tool design</a>).</li>
  <li><strong>Human checkpoints</strong>: which steps wait, for whom, in which tool, with what deadline and fallback.</li>
  <li><strong>Data and retrieval</strong>: what documents the system must consult, how they are indexed, how freshness is maintained.</li>
  <li><strong>Security</strong>: credentials per tool, what leaves your cloud account (ideally nothing), retention of logs and documents.</li>
  <li><strong>Cost model</strong>: model cost per item, infrastructure cost per month, human review minutes per item, compared against the current cost per item.</li>
  <li><strong>Evaluation</strong>: the test set, the accuracy bar, and who signs off.</li>
</ol>

<h2>Step 4: build the cost model honestly</h2>
<p>An automation that costs more than the work it replaces is a science project. The numbers that matter per item:</p>
<pre><code>current_cost   = minutes_per_item × loaded_hourly_rate / 60
automated_cost = model_cost_per_item
               + infra_cost_per_month / items_per_month
               + review_rate × review_minutes × loaded_hourly_rate / 60
savings        = (current_cost − automated_cost) × items_per_month</code></pre>
<p>Model cost is usually the smallest term; review rate is the one to design around. A system that sends 30% of items to a human is still a large saving if those 30% took 90% of the time before.</p>

<h2>Step 5: build spoke by spoke</h2>
<p>Do not build the whole flow and then switch it on. Sequence it so that value lands early and risk stays contained:</p>
<ol>
  <li><strong>Read-only assistant.</strong> The system extracts, matches and prepares; a person still does every commit. This alone often halves handling time and produces the evaluation data you need.</li>
  <li><strong>Auto-commit for the safe path.</strong> Items that pass every rule and fall under the risk threshold commit without review. Everything else goes to the queue as before.</li>
  <li><strong>Widen the safe path.</strong> Use the review log to find exception types worth automating; add a spoke for each.</li>
</ol>

<h2>Step 6: operate it like a system, not a script</h2>
<ul>
  <li>Dashboards for volume, straight-through rate, review queue age, cost per item and error types.</li>
  <li>Alerts on budget overrun, tool failures and review queue backlog.</li>
  <li>A weekly review of rejected items; each recurring rejection is a candidate rule or spoke.</li>
  <li>Re-run the evaluation set on every prompt, model or tool change.</li>
  <li>Documentation and training so the process owner, not the vendor, owns the system.</li>
</ul>

<h2>Worked example: supplier invoice intake</h2>
<p><strong>Before:</strong> two people spend most of each morning opening invoice PDFs from a shared mailbox, keying vendor, total and PO number into the ERP, checking the purchase order, and chasing mismatches by email. Roughly 12 minutes per invoice, 60 invoices a day.</p>
<p><strong>After:</strong> a mailbox trigger hands each PDF to a documents spoke that extracts fields with structured output; a rules step checks the PO match and tolerance; matches under the approval limit post automatically; mismatches and high-value items land in a review queue with the extracted data and the reason attached. Human time drops to a few minutes per exception; the straight-through rate settles around 70% after the second month as recurring exceptions get their own rules.</p>
<p>The architecture is not exotic. The discipline is in the mapping, the boundaries and the cost model, which is why we spend the first phase there.</p>
''',
 'faq': [
  ('Which processes are the best first candidates for AI automation?', 'Frequent, mostly rule-following processes with a few judgement calls and visible cost: invoice intake, support triage, vendor onboarding, order exceptions and contract intake. Avoid starting with rare or highly consequential decisions.'),
  ('Do we need to replace our ERP or helpdesk?', 'No. The architecture wraps existing systems with typed tools; the process runs where the work already happens. Replacing systems of record is almost never a prerequisite.'),
  ('How long until the first process is live?', 'A read-only assistant for one process is typically live within weeks of discovery; auto-commit for the safe path follows once the evaluation set confirms accuracy and the review data supports the threshold.'),
 ],
},
]
