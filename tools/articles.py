# Article content for /insights. Edit here, then run tools/build_insights.py.

ARTICLES = [
{
 'slug': 'designing-the-agent-team',
 'short': 'Designing the agent team',
 'kicker': 'Agent team design',
 'title': 'Designing the agent team: roles, scope and handoffs',
 'desc': 'Before any code is written, an agentic system is a set of decisions about roles: which agents exist, what each one may read and change, where it must stop, and how work moves between them. This is the method we use to turn a real process into an agent team.',
 'date': '2026-09-22',
 'read': 9,
 'about': ['Agentic systems', 'AI agent design', 'Multi-agent systems'],
 'keywords': ['agent team design', 'AI agent roles', 'multi-agent system design', 'agent scope', 'handoffs', 'orchestrator'],
 'body': '''
<h2>The design happens before the prompt</h2>
<p>Most failed agent projects were lost at the whiteboard, not in the code. Someone picked a framework, wired up four agents that sounded sensible, and discovered three months later that nobody could say which agent was responsible for a wrong result. An agent team is an organisational design problem first: roles, authority, handoffs and escalation. The prompts come last, and they get much easier once the roles are right.</p>
<p>This article describes the method we use in the design phase of a build: how a real process becomes a set of agent roles with boundaries you can test and audit.</p>

<h2>Start from the process, not the org chart</h2>
<p>Map the process as it is actually performed, with the people who perform it, step by step. For each step, record four things:</p>
<ul>
  <li><strong>Input</strong>: what arrives, in what form, from where.</li>
  <li><strong>Decision</strong>: what judgment the step requires, if any.</li>
  <li><strong>Effect</strong>: what changes in the world when the step completes.</li>
  <li><strong>Reversibility</strong>: how expensive it is to undo that effect.</li>
</ul>
<p>Do not model the departments. A process that crosses finance and procurement does not need a "finance agent" and a "procurement agent" because the company has those two teams. It needs agents shaped like the work: a document agent that reads what arrived, a matching agent that reconciles it against a record, a posting agent that writes to a system of record.</p>

<h2>What makes a good agent role</h2>
<p>A role is well drawn when you can write a single sentence of the form "this agent turns X into Y, and may touch nothing else." Four properties follow from that:</p>
<ul>
  <li><strong>One job.</strong> If the role description contains "and also", split it.</li>
  <li><strong>Bounded input.</strong> The agent receives a defined payload, not "the conversation so far".</li>
  <li><strong>Explicit authority.</strong> The tools it may call are listed, and nothing else is reachable.</li>
  <li><strong>A stopping condition.</strong> The agent knows what "done" looks like and what to do when it cannot get there.</li>
</ul>
<p>Roles that violate these are usually too large. An agent asked to "handle vendor onboarding end to end" will improvise; three agents with narrow jobs and an orchestrator that sequences them will not.</p>

<h2>The authority table</h2>
<p>For every agent, fill in one row before any implementation starts. This table becomes the permission model, the test plan and the thing you show a security reviewer.</p>
<table>
  <thead><tr><th>Agent</th><th>May read</th><th>May change</th><th>Decides</th><th>Must escalate when</th></tr></thead>
  <tbody>
    <tr><td>Documents</td><td>Inbox folder, document store</td><td>Nothing</td><td>Document type, extracted fields</td><td>Confidence below threshold, unreadable file</td></tr>
    <tr><td>Matching</td><td>Extracted fields, purchase orders</td><td>Nothing</td><td>Match / no match, discrepancy list</td><td>Partial match, price variance over tolerance</td></tr>
    <tr><td>Posting</td><td>Matched record</td><td>ERP: create draft, post</td><td>Nothing</td><td>Always, above the approval threshold</td></tr>
  </tbody>
</table>
<p>Two rules make this table useful rather than decorative. First, <strong>permissions belong to tools, not to agents</strong>: the posting agent cannot post because the model decided to, it can post because the tool it is allowed to call performs exactly that operation and nothing wider. Second, <strong>read and write are separate tools</strong>, ideally separate servers, so a read-only agent cannot be talked into writing.</p>

<h2>Handoffs are contracts, not conversations</h2>
<p>The weakest point in most multi-agent systems is the handoff. Agents pass each other free text, the next agent re-interprets it, and small misunderstandings compound. Treat every handoff as a typed payload with a schema: what fields, what types, what is required, what a failure looks like.</p>
<p>In a <a href="/insights/hub-and-spoke-agent-architecture/">hub-and-spoke team</a> the handoff is always agent to orchestrator and back, never agent to agent. That single rule removes an entire class of debugging: when the output is wrong, the orchestrator's log shows exactly which payload entered which agent and what came out.</p>
<p>A good handoff payload also carries provenance: which document, which record id, which confidence, which model produced it. When a human reviews the result later, they should not have to re-derive where a number came from.</p>

<h2>Where the team ends and a person begins</h2>
<p>Every design has a line past which the system does not act alone. Draw it with the reversibility column from your process map, not with intuition. Steps that are cheap to undo (drafting, classifying, gathering) can run unattended. Steps that move money, contact a customer, or create a record other systems depend on wait for a person.</p>
<p>Two distinct mechanisms are involved, and they are often confused. An <strong>approval gate</strong> is planned: the system knows in advance that this step requires a signature, and the work stops there by design. A <strong>delegation to a human</strong> is dynamic: the agent has hit a case it cannot resolve and hands it to a person mid-flight. The first is covered in <a href="/insights/human-in-the-loop-for-agentic-systems/">human-in-the-loop design</a>; the second is a capability the team needs from day one, described in <a href="/insights/delegate-to-human/">delegating to a human</a>.</p>

<h2>How many agents?</h2>
<p>Fewer than people expect. A useful heuristic: one agent per distinct <em>skill set</em> in the process, not one per step. If two steps require the same knowledge and the same tools, they belong to the same agent. If a step needs different context, different tools or a different risk level, split it out.</p>
<p>Four to six specialist agents covers most back-office processes. Beyond that, ask whether you have discovered a second process wearing the first one's clothes, and whether it deserves its own team.</p>

<h2>Test the design before you build it</h2>
<p>You can evaluate a role design on paper. Take ten real cases from the last month, including the three that went wrong, and walk them through the roles you drew:</p>
<ul>
  <li>Does every case reach a terminal state, or do some fall between two agents?</li>
  <li>Can you name, for each case, the single agent accountable for the outcome?</li>
  <li>Does any agent need data it has no permission to read?</li>
  <li>Which cases hit an escalation, and does a person have enough context to act?</li>
</ul>
<p>Cases that stall in this exercise will stall in production. Redraw the roles now, while the design is a table and not a codebase.</p>

<h2>What you take into the build</h2>
<p>The output of a design phase is small and concrete: a process map, an authority table, a handoff schema per edge, a list of escalation conditions, and ten test cases with known correct outcomes. With those in hand, building the team becomes an ordinary engineering task, and the first evaluation run has something to measure against.</p>
''',
 'faq': [
  ('How long does designing an agent team take?', 'For one process, usually one to two weeks of part-time work with the people who run it. The output is a process map, an authority table per agent, handoff schemas and a test set. That artefact is what makes the build predictable, and it is worth keeping even if you decide not to build.'),
  ('Should each agent have its own model?', 'Not necessarily its own model, but usually its own model choice. The orchestrator benefits from a stronger model because it plans and verifies; narrow specialists often run well on smaller, cheaper ones. Decide per role against the evaluation set rather than standardising on one model everywhere.'),
  ('What if the process is not documented anywhere?', 'That is the normal case. The design phase doubles as documentation: mapping the process with the people who perform it usually surfaces exceptions and informal rules that were never written down, and those exceptions are exactly what determines the agent boundaries.'),
 ],
},
{
 'slug': 'hub-and-spoke-agent-architecture',
 'short': 'Hub-and-spoke agent architecture',
 'kicker': 'Architecture',
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
 'slug': 'agent-topologies',
 'short': 'Agent team topologies',
 'kicker': 'Architecture',
 'title': 'Agent team topologies: which hierarchy to build, and when',
 'desc': 'Hub-and-spoke is a good default, not the only shape. Single agents, two-level hierarchies, pipelines, blackboards and swarms each solve a different problem and fail in a different way. Here is how to choose the topology before you commit to it.',
 'date': '2026-09-22',
 'read': 8,
 'about': ['Multi-agent systems', 'Agentic architecture', 'AI orchestration'],
 'keywords': ['agent topology', 'hierarchical agents', 'multi-agent architecture', 'orchestrator', 'agent pipeline', 'swarm agents'],
 'body': '''
<h2>Topology is a decision, not a default</h2>
<p>Ask five teams how their agents are wired and you will get five answers, most of them accidental: whatever the framework's tutorial did. Topology deserves an explicit decision, because it determines how the system fails, how much it costs per run, and how hard it is to add the next capability.</p>
<p>Five shapes cover almost everything worth building. Each has a natural fit and a characteristic failure.</p>

<h2>1. Single agent with tools</h2>
<p>One model, a list of typed tools, a loop. No delegation, no sub-agents.</p>
<p><strong>Fits:</strong> a bounded task with one skill set: classify an email and file it, extract fields from a document, answer from a knowledge base. If the whole job fits in one agent's context and permission set, adding agents adds only latency.</p>
<p><strong>Fails when:</strong> the tool list grows past roughly a dozen and the agent starts choosing badly, or when two parts of the task need different permissions and you can no longer scope them separately.</p>
<p><strong>Rule of thumb:</strong> start here. Most "we need a multi-agent system" requests are one agent with a well-designed tool set.</p>

<h2>2. Hub-and-spoke</h2>
<p>One orchestrator plans, routes and verifies; specialist agents, tool servers and human reviewers are spokes that only ever talk to the hub.</p>
<p><strong>Fits:</strong> a process that crosses several systems, has steps at different risk levels, and must be explainable afterwards. This is the working default for back-office automation, and the pattern is described in detail in <a href="/insights/hub-and-spoke-agent-architecture/">hub-and-spoke agent architecture</a>.</p>
<p><strong>Fails when:</strong> the hub becomes a bottleneck of context. Every result passes through it, so a process with dozens of steps and large payloads will strain the orchestrator's context window and cost.</p>

<h2>3. Two-level hierarchy</h2>
<p>An orchestrator delegates to team leads, each of which owns a group of specialists and returns one consolidated result.</p>
<pre><code>orchestrator
├── intake lead
│   ├── document specialist
│   └── classification specialist
└── finance lead
    ├── matching specialist
    └── posting specialist</code></pre>
<p><strong>Fits:</strong> processes too large for one hub's context, or organisations where different departments own different halves of a flow and want separate evaluation sets, permissions and release cycles.</p>
<p><strong>Fails when:</strong> the hierarchy is built for tidiness rather than need. Every extra level adds a summarisation step, and every summarisation loses detail. Two levels is almost always enough; three is a sign the process should be split into two systems.</p>
<p>A second level earns its place when the lead does real work: it holds context its specialists do not need, it makes routing decisions, and it can fail a whole branch without the orchestrator re-planning from scratch.</p>

<h2>4. Pipeline</h2>
<p>A fixed sequence of stages, each transforming the payload and passing it on. No planning at run time.</p>
<p><strong>Fits:</strong> high-volume, low-variance work where the steps never change: ingest, extract, validate, enrich, store. A pipeline is cheaper and far more predictable than an orchestrated team because there is no planning token spend and no route to get wrong.</p>
<p><strong>Fails when:</strong> real cases need to skip, repeat or branch. The moment you add conditional routing to a pipeline you are building an orchestrator, and you should build it deliberately.</p>
<p>Many production systems are a pipeline with one orchestrated stage in the middle, which is a good outcome: keep the deterministic parts deterministic.</p>

<h2>5. Blackboard (shared state)</h2>
<p>Agents read from and write to a shared, structured workspace instead of passing payloads directly. A controller decides who runs next based on what is on the board.</p>
<p><strong>Fits:</strong> long-running cases that accumulate evidence over hours or days: an investigation, a claim, a diligence file. State outlives any single run, and different agents contribute as information arrives.</p>
<p><strong>Fails when:</strong> the board has no schema. Untyped shared state degrades into a junk drawer, and agents begin depending on fields they did not agree on. If you use this shape, version the board like a database, because it is one.</p>

<h2>6. Swarm, and why we avoid it</h2>
<p>Any agent may call any other agent. It demos beautifully.</p>
<p><strong>Fails when:</strong> anything goes wrong. There is no single place that knows the plan, so you cannot answer "why did it do that", cycles are easy to create and hard to detect, permissions cannot be reasoned about (any agent can reach any capability transitively), and cost per run is unbounded. We do not build these for production processes.</p>

<h2>Choosing</h2>
<table>
  <thead><tr><th>If the process…</th><th>Build</th></tr></thead>
  <tbody>
    <tr><td>Is one task with one skill set</td><td>Single agent with tools</td></tr>
    <tr><td>Crosses systems, mixed risk, must be auditable</td><td>Hub-and-spoke</td></tr>
    <tr><td>Is too large for one hub, or split across owners</td><td>Two-level hierarchy</td></tr>
    <tr><td>Is high volume and never branches</td><td>Pipeline</td></tr>
    <tr><td>Accumulates evidence over days</td><td>Blackboard with a schema</td></tr>
  </tbody>
</table>

<h2>Migrating between shapes</h2>
<p>Topologies are not permanent, and the migrations are asymmetric. Single agent to hub-and-spoke is easy if your tools were typed from the start: the tools stay, the loop moves into an orchestrator. Hub-and-spoke to two levels is easy if handoffs already had schemas: you insert a lead that speaks the same contract. Anything to swarm is easy and anything from swarm is a rewrite.</p>
<p>That asymmetry is the practical argument for typed tool contracts and schema-bearing handoffs even in a system that starts as one agent: they are what makes the next shape a refactor rather than a restart.</p>
''',
 'faq': [
  ('Is more agents always better?', 'No. Every agent adds a handoff, a summarisation step and latency. Add an agent when a part of the work needs a different skill set, different tools or a different risk level, not to make a diagram look thorough.'),
  ('Can one system use more than one topology?', 'Usually it should. A common production shape is a deterministic pipeline for ingestion with one orchestrated stage where judgment is required, and a human approval gate before anything is written. Use the cheapest shape that each part of the work allows.'),
  ('How do I know the orchestrator has become a bottleneck?', 'Watch context size and planning cost per run. If the orchestrator spends most of its tokens restating results it just received, or if adding a step forces you to trim earlier context, it is time for a second level or for splitting the process.'),
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

<p class="callout">A small, runnable reference implementation of these rules on an invoice-intake process is open source: <a href="https://github.com/justdukkan/invoice-intake-mcp">github.com/justdukkan/invoice-intake-mcp</a>.</p>

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
 'slug': 'connecting-agents-to-your-apis',
 'short': 'Connecting agents to your APIs',
 'kicker': 'Integration',
 'title': 'Connecting agents to your APIs: identity, idempotency and the failures nobody plans for',
 'desc': 'An agent team is only as good as its connection to the systems that hold the work. These are the integration rules we apply when agents start calling a company\'s CRM, ERP, helpdesk and internal APIs: who they act as, what happens on a retry, and how failures are made legible.',
 'date': '2026-09-22',
 'read': 8,
 'about': ['API integration', 'AI agent security', 'Agentic systems'],
 'keywords': ['agent API integration', 'MCP server', 'idempotency', 'service account', 'rate limits', 'typed errors'],
 'body': '''
<h2>The integration is most of the work</h2>
<p>Demos run against toy data. Production agents run against a CRM with fifteen years of exceptions in it, an ERP that rejects a posting for reasons no one can explain, and an internal API whose documentation stopped matching reality in 2022. The model is rarely the hard part. The integration is.</p>
<p>Everything below assumes agents reach systems through typed tools, usually exposed as <a href="/insights/mcp-server-and-tool-design/">MCP servers</a>, rather than by being handed raw HTTP access. That boundary is what makes the rest of this enforceable.</p>

<h2>Identity: who is the agent acting as?</h2>
<p>Answer this before writing a line of integration code. Three options, in descending order of how much we like them:</p>
<ul>
  <li><strong>On behalf of a person.</strong> The agent uses a token scoped to the requesting user, so existing permissions apply unchanged and the audit trail in the target system names a real human. Best when it is available.</li>
  <li><strong>A dedicated service identity per agent role.</strong> The posting agent has its own account with exactly the rights to post, and nothing else. Logs in the ERP show which agent role acted.</li>
  <li><strong>One shared service account for everything.</strong> Common, and the source of most integration incidents. Every agent inherits every permission, and the audit trail says only "integration user".</li>
</ul>
<p>Whichever you pick, the credential lives in the tool server, never in a prompt, never in the model's context, and never in a log line.</p>

<h2>Scopes follow the authority table</h2>
<p>The permission model you drew during <a href="/insights/designing-the-agent-team/">agent team design</a> should map one to one onto API scopes. If the matching agent may read purchase orders and change nothing, its credential has read scope on purchase orders and no write scope anywhere. Do not rely on the tool implementation to be the only thing standing between an agent and a destructive call: the server should be unable to perform the call, not merely unwilling.</p>
<p>The practical form of this is a read server and a write server, separately credentialed. Read-only agents connect to the first and cannot reach the second.</p>

<h2>Idempotency: the retry problem</h2>
<p>Agents retry. Networks time out, models produce a malformed argument and try again, an orchestrator re-plans after a partial failure. Without idempotency this means duplicate invoices, duplicate tickets, duplicate emails.</p>
<p>Every write tool needs a deterministic idempotency key derived from the business fact, not from the attempt. For an invoice posting, something like <code>supplier_id + invoice_number</code>; for a reply, the ticket id plus a content hash. The tool passes it to the API where the API supports it, and where it does not, the tool keeps its own record of keys already committed and returns the previous result instead of acting twice.</p>
<pre><code>post_invoice(
  idempotency_key = "SUP-4412:INV-2026-0918",
  ...
)
# second call with the same key returns the first result,
# marked as a replay, and changes nothing</code></pre>
<p>Make the replay visible in the return value. An agent that cannot tell "I posted it" from "it was already posted" will narrate the wrong thing to a human later.</p>

<h2>Typed errors, not prose</h2>
<p>An API that answers a bad request with a 400 and an HTML error page gives the agent nothing to act on, so it guesses. Tools should translate every failure into a small, closed set of typed errors that say what to do next:</p>
<ul>
  <li><code>not_found</code>: the record does not exist. Stop, report.</li>
  <li><code>validation_failed</code>: with the offending field. Fix and retry once.</li>
  <li><code>permission_denied</code>: never retry, escalate.</li>
  <li><code>conflict</code>: someone else changed the record. Re-read, then decide.</li>
  <li><code>rate_limited</code>: with a wait hint. Back off.</li>
  <li><code>upstream_unavailable</code>: retry with backoff, then escalate.</li>
</ul>
<p>Each error should carry a human-readable message for the escalation path and a machine-readable code for the agent. The difference between an agent that recovers and an agent that loops is almost always the quality of this taxonomy.</p>

<h2>Rate limits and backpressure</h2>
<p>An agent can generate a year of a human's API traffic in an afternoon. Assume you will hit limits and design for it: a concurrency cap per tool server, exponential backoff with jitter, a queue with a visible depth, and a circuit breaker that stops a run rather than hammering a degraded system. Tell the orchestrator when work is deferred, so it reports "waiting on the ERP" instead of silently stalling.</p>

<h2>Reads are not free either</h2>
<p>Large result sets are a context problem, not just a cost problem. Tools should paginate, accept filters that push work to the API, and return summaries with a handle for detail rather than dumping ten thousand rows into an agent's context. A good read tool answers "which invoices are unmatched this week" with twenty rows and a count, not with the table.</p>

<h2>Events coming the other way</h2>
<p>Most integrations eventually need inbound events: a ticket created, an invoice received, a record changed. Treat webhooks as a first-class part of the integration, with the same discipline as outbound calls: verify signatures, deduplicate by event id, accept fast and process asynchronously, and make replay safe. An agent team that reacts to events needs the same idempotency guarantees as one that writes.</p>

<h2>Test against something real</h2>
<p>Mocked integrations pass and production fails, because the interesting behaviour lives in the exceptions. Get a sandbox tenant if the vendor offers one, a replica if they do not, and build the evaluation set from real historical cases including the ones that errored. Every typed error above should appear in at least one test case, with an assertion about what the agent does next.</p>

<h2>Integration checklist</h2>
<ul>
  <li>Identity decided and scoped per agent role; credentials only in the tool server.</li>
  <li>Read and write separated, with separate credentials.</li>
  <li>Idempotency key on every write, replays visible in the response.</li>
  <li>Closed set of typed errors with a defined agent reaction to each.</li>
  <li>Backoff, concurrency cap and circuit breaker on every external call.</li>
  <li>Pagination and filtering on every read; no unbounded result into context.</li>
  <li>Inbound events deduplicated and signature-verified.</li>
  <li>Evaluation set built from real cases, including failures.</li>
  <li>Every call logged with actor, arguments, result and duration.</li>
</ul>
<p>None of this is specific to AI. It is ordinary integration engineering, applied to a caller that is faster, more literal and less embarrassed to retry than any human user you have integrated for before.</p>
''',
 'faq': [
  ('Should agents call our APIs directly instead of through MCP servers?', 'We do not recommend it. A tool server is where permissions, idempotency, error translation, rate limiting and logging live. Handing an agent raw HTTP access means every one of those concerns has to be enforced by prompt instructions, which is not enforcement.'),
  ('What if the internal API has no idempotency support?', 'Then the tool server provides it: keep a record of committed idempotency keys with the result of the original call, and return that result on a repeat instead of calling the API again. It is a small table and it prevents the most expensive class of agent incident.'),
  ('How do we handle APIs that are slow or frequently down?', 'Treat unavailability as a normal path, not an exception. Queue the work, report the delay to the orchestrator so the run shows as waiting rather than failed, apply backoff with a circuit breaker, and define an escalation after a threshold so a person learns about it before the customer does.'),
 ],
},
{
 'slug': 'agent-skills',
 'short': 'Agent skills',
 'kicker': 'Build',
 'title': 'Agent skills: packaging repeatable expertise so agents stop improvising',
 'desc': 'A tool is something an agent can do. A skill is how your company does it. Skills capture the procedure, the exceptions and the house rules as versioned, testable artefacts, so the same case does not get handled three different ways.',
 'date': '2026-09-22',
 'read': 7,
 'about': ['Agentic systems', 'AI agent design', 'Prompt engineering'],
 'keywords': ['agent skills', 'agent instructions', 'prompt versioning', 'tool design', 'procedures', 'agentic systems'],
 'body': '''
<h2>Tools, skills and instructions</h2>
<p>Three things get confused because they all end up in an agent's context. It is worth keeping them apart:</p>
<ul>
  <li>A <strong>tool</strong> is a capability: a typed operation the agent can invoke, like <code>erp.post_invoice</code>. It is code.</li>
  <li>A <strong>skill</strong> is a procedure: how your company handles a recurring situation, which tools it uses in what order, what the exceptions are, what "done" looks like. It is content, loaded when relevant.</li>
  <li>The <strong>instructions</strong> are the agent's standing identity and constraints, always present.</li>
</ul>
<p>Teams that only have tools and instructions end up with enormous prompts that try to describe every procedure at once, and agents that improvise when a case does not match. Skills are how you stop that.</p>

<h2>What a skill contains</h2>
<p>A skill is a short document with a name, a description of when it applies, and the procedure itself. The description matters as much as the body: it is what lets the agent decide the skill is relevant. Vague descriptions produce skills that never load or load at the wrong time.</p>
<pre><code>name: supplier-credit-note
when: an incoming document is a credit note from a supplier,
      or an invoice that references an earlier invoice number
procedure:
  1. Match to the original invoice by supplier and invoice number.
  2. If the original was already posted, create an offset draft.
  3. If it was not posted, cancel the draft and note the reason.
  4. Credit notes above the approval threshold always go to review.
exceptions:
  - Multiple originals: never guess, escalate with both candidates.
  - Currency differs from the original: escalate.</code></pre>
<p>Notice what is not in it: no model instructions, no personality, no restating of permissions. Skills describe the work, not the agent.</p>

<h2>Why not put all of this in the prompt?</h2>
<p>Three reasons, in increasing order of importance.</p>
<p><strong>Context cost.</strong> Twenty procedures in one prompt means paying for twenty procedures on every request, including the nineteen that are irrelevant.</p>
<p><strong>Interference.</strong> Procedures that are all present at once bleed into each other. The credit-note rule leaks into ordinary invoice handling, and you debug it by nudging wording, which breaks something else.</p>
<p><strong>Ownership.</strong> A prompt is an engineering artefact. A skill can be reviewed, corrected and approved by the person who actually owns the process. When the finance lead says "we changed the threshold", that is a one-line edit to a document with a version history, not a ticket for the AI team.</p>

<h2>Version them like code, review them like policy</h2>
<p>Skills live in version control, go through review, and carry a changelog. The reviewer is not only an engineer: the process owner signs off on the procedure, because it is their procedure. Every change gets an entry in the evaluation set, so "we tightened the credit-note rule" is a measurable change rather than a hopeful one.</p>
<p>This matters more than it sounds. Most of the drift in a live agent system is not model drift, it is procedure drift: the business changed a rule in March and nobody told the system. Versioned skills with named owners are how that gets caught in review instead of in an audit.</p>

<h2>Testing a skill</h2>
<p>A skill is testable in a way a personality prompt is not, because it makes claims about specific cases. For each skill, keep a handful of real cases and assert the outcome:</p>
<ul>
  <li>Cases the skill should handle end to end, with the expected result.</li>
  <li>Cases that should trigger each listed exception, with the expected escalation.</li>
  <li>Near-miss cases that should <em>not</em> load this skill at all, to catch over-broad descriptions.</li>
</ul>
<p>That last category is the one people skip and the one that finds real bugs. A skill whose description is too generous will capture cases meant for another procedure, and the failure looks like the model being wrong rather than the routing being wrong.</p>

<h2>When a skill should become a tool</h2>
<p>If a procedure has no judgment in it, stop writing it as a skill and write it as code. A skill that says "call these three tools in this order, always" is a tool that has not been created yet. Deterministic sequences belong in a tool: they are cheaper, faster and cannot be done slightly differently on a bad day.</p>
<p>The reverse test is just as useful. If a tool keeps needing prose in the prompt to explain when to use it and what to do with the result, that prose is a skill trying to exist.</p>

<h2>How many skills?</h2>
<p>One per recurring situation that a new employee would need explained to them. In practice a mature back-office agent team runs on somewhere between five and twenty, most of them under a page. If a skill is growing past two pages, it is usually two skills, or it contains a procedure that should be a tool.</p>

<h2>The payoff</h2>
<p>Skills turn "the AI handled it differently this time" into a question with an answer: which skill applied, what version was it, who approved that version, and what did the evaluation set say when it changed. That traceability is what lets a company hand a real process to an agent team and still be able to explain, months later, why a particular case went the way it did. It is also the layer that changes most often in <a href="/insights/operating-agentic-systems/">ongoing maintenance</a>, which is why it is worth designing as a first-class artefact rather than as prompt text.</p>
''',
 'faq': [
  ('Is a skill the same thing as a prompt template?', 'No. A template shapes how a single request is phrased. A skill is a durable description of a procedure: when it applies, which tools it uses, what the exceptions are, and what the finished state looks like. It is loaded only when relevant, versioned, and owned by the person who owns the process.'),
  ('Who should write the skills?', 'The process owner writes the procedure, an engineer shapes it into the structure the agent can act on, and both review changes. Skills written entirely by engineers tend to miss the exceptions that make the process real; skills written entirely by process owners tend to omit the tool boundaries.'),
  ('How do skills interact with permissions?', 'They do not grant anything. Permissions live on tools, so a skill can describe a procedure an agent is not allowed to complete, and the tool call will fail. That is intentional: the skill says what should happen, the permission model decides what can.'),
 ],
},
{
 'slug': 'delegate-to-human',
 'short': 'Delegating to a human',
 'kicker': 'Human in the loop',
 'title': 'Delegate to human: making escalation a first-class capability',
 'desc': 'Approval gates are planned. Delegation is not: it is what happens when an agent meets a case it should not resolve alone. Treating "hand this to a person" as a real tool, with a payload, an owner and a return path, is what separates an agent team that degrades gracefully from one that guesses.',
 'date': '2026-09-22',
 'read': 7,
 'about': ['Agentic systems', 'Human-in-the-loop', 'AI operations'],
 'keywords': ['delegate to human', 'agent escalation', 'human in the loop', 'agentic systems', 'exception handling', 'handoff'],
 'body': '''
<h2>Two different things called "human in the loop"</h2>
<p>An <strong>approval gate</strong> is designed in advance. The system knows that posting an invoice over a threshold requires a signature, so the run stops there every time, by policy. That is covered in <a href="/insights/human-in-the-loop-for-agentic-systems/">human-in-the-loop for agentic systems</a>.</p>
<p><strong>Delegation</strong> is dynamic. The agent is midway through a case, encounters something outside what it can responsibly resolve, and hands the work to a person. Nothing in the plan predicted this particular case. The question is not whether the agent is allowed to act; it is whether it should.</p>
<p>Systems that implement only the first behave badly in the wild, because the interesting failures are exactly the unplanned ones. An agent with no way to delegate has exactly two options in an ambiguous case: guess, or fail. Both are worse than asking.</p>

<h2>Escalation is a tool, not a fallback</h2>
<p>Give the agent an actual tool, listed alongside the others, with a schema:</p>
<pre><code>delegate_to_human(
  reason,            # one of a closed set
  summary,           # what the agent was doing
  blocking_question, # what it needs decided
  options,           # candidate answers, if any
  evidence,          # links, record ids, extracted values
  suggested_owner    # role or queue
)</code></pre>
<p>Making it a tool has three effects. The agent can choose it explicitly rather than drifting into an error path. The call is logged like any other, so you can measure it. And the payload is structured, which is what makes the human side fast.</p>

<h2>When should an agent delegate?</h2>
<p>Do not leave this to the model's judgment alone. Enumerate the reasons, and make them a closed set so they can be counted:</p>
<ul>
  <li><strong>Low confidence</strong> on an extraction or classification that drives a consequential step.</li>
  <li><strong>Ambiguity</strong>: more than one plausible match, and choosing wrong is expensive.</li>
  <li><strong>Missing information</strong> that no available tool can supply.</li>
  <li><strong>Policy edge</strong>: the case is near a threshold or outside the documented procedure.</li>
  <li><strong>Conflicting sources</strong>: two systems disagree about the same fact.</li>
  <li><strong>Repeated failure</strong>: the same step has failed twice and a third attempt will not help.</li>
  <li><strong>Novelty</strong>: no skill matches this situation at all.</li>
</ul>
<p>Each reason should also appear in the evaluation set, with cases that must trigger it. An agent that never delegates is not confident, it is uninstrumented.</p>

<h2>What the human receives</h2>
<p>The quality of a delegation is judged by how long it takes a person to act on it. A good handoff answers, without any clicking: what is this case, what has already happened, what exactly is being asked, what are the candidate answers, and what happens after I answer.</p>
<p>A bad handoff says "unable to process invoice, please check". The person then repeats the agent's work from scratch, which costs more than if the agent had never started.</p>
<p>Two practical rules. Ask <strong>one</strong> question per delegation; if two decisions are needed, either ask them together with both sets of options or split into two cases. And offer <strong>options rather than an open field</strong> wherever the answer is from a known set, because a structured answer can be fed straight back into the run.</p>

<h2>The return path</h2>
<p>Delegation is only half a mechanism. The run has to survive the wait and resume correctly, which means:</p>
<ul>
  <li><strong>State is persisted</strong>, not held in a conversation. The case may wait overnight.</li>
  <li><strong>Partial work is not lost.</strong> Whatever the agent established before delegating is still valid when the answer arrives.</li>
  <li><strong>The answer is recorded as provenance</strong>: who decided, when, what they chose, and against what evidence.</li>
  <li><strong>There is a timeout.</strong> A case that waits three days should re-route or surface on a dashboard, not sit silently.</li>
  <li><strong>Nothing half-applied.</strong> If the agent had already written something before it got stuck, the delegation says so explicitly.</li>
</ul>

<h2>Routing: who gets asked</h2>
<p>"A human" is not an address. Delegations go to a role or a queue with an owner, chosen by reason and by case: a pricing question goes to the category buyer, a compliance flag to the compliance queue. If the system cannot decide, it should have a default queue rather than a default person, so that holidays and departures do not create silent black holes.</p>

<h2>Delegation rate is a metric, not a defect</h2>
<p>Track it. The number is diagnostic in both directions.</p>
<table>
  <thead><tr><th>Pattern</th><th>Usually means</th></tr></thead>
  <tbody>
    <tr><td>Rate climbing over weeks</td><td>The process changed and the skills did not</td></tr>
    <tr><td>Rate near zero</td><td>Thresholds too loose; check for wrong answers accepted silently</td></tr>
    <tr><td>One reason dominating</td><td>A fixable gap: a missing tool, a bad data source, an unclear rule</td></tr>
    <tr><td>Same case type every week</td><td>A skill waiting to be written</td></tr>
  </tbody>
</table>
<p>In the first weeks of a live system the delegation rate should be high and falling. Each cluster of delegations tells you what the next skill, tool or threshold change should be, which makes this one of the most useful signals a running agent team produces.</p>

<h2>The design principle</h2>
<p>An agent that can say "I should not decide this" is more useful than one that always produces an answer, because the second kind forces people to check everything, and checking everything costs more than doing it. Build the escalation path on day one, measure it, and let it shrink as the system learns the work.</p>
''',
 'faq': [
  ('How is this different from an approval gate?', 'An approval gate is a planned stop: the policy says this step always needs a signature. A delegation is unplanned: the agent has met a case it should not resolve on its own. A system needs both, and they have different payloads, different routing and different metrics.'),
  ('Does delegation slow the process down?', 'It replaces an invisible wrong answer with a visible short wait. In practice, well-routed delegations with a complete payload are resolved in minutes, and the total cycle time still falls because the cases that used to be re-checked by hand no longer are.'),
  ('Should the agent try to resolve ambiguity by asking more tools first?', 'Yes, up to a point. Cheap, safe reads that could resolve the question should be attempted before escalating, and the delegation payload should record what was already tried. Repeating the same failing call is not investigation.'),
 ],
},
{
 'slug': 'human-in-the-loop-for-agentic-systems',
 'short': 'Human-in-the-loop design',
 'kicker': 'Human in the loop',
 'title': 'Human-in-the-loop for agentic systems: where people belong, and where they only slow things down',
 'desc': '"Keep a human in the loop" is easy to say and usually done badly: either every step waits for someone, or nothing does. This is how we decide which decisions get a human checkpoint, how the checkpoint is built so it is actually used, and how the loop shrinks over time without losing control.',
 'read': 8,
 'about': ['Human-in-the-loop', 'AI governance', 'Agentic systems'],
 'keywords': ['human in the loop', 'HITL', 'AI approval workflow', 'agent guardrails', 'risk threshold', 'agentic automation'],
 'body': """
<h2>Two ways to get it wrong</h2>
<p><strong>Everything waits.</strong> The system prepares work and a person approves each item. Handling time drops a little, the review queue becomes the bottleneck, reviewers start approving without reading, and the checkpoint stops meaning anything. The company paid for automation and got a rubber stamp.</p>
<p><strong>Nothing waits.</strong> The system acts end to end. The first bad outcome that reaches a customer, an auditor or a bank account ends the project, regardless of how well the other thousand items went.</p>
<p>The useful version sits between the two: humans decide exactly where the consequence of a wrong action is real and hard to reverse, and nowhere else.</p>

<h2>Classify decisions by consequence, not by difficulty</h2>
<p>The instinct is to send "hard" decisions to people. Difficulty is the wrong axis; models are often better than tired humans at hard-but-bounded judgement. The right axis is what happens if the decision is wrong:</p>
<table>
  <tr><th>If wrong…</th><th>Example</th><th>Who decides</th></tr>
  <tr><td>Nothing leaves the system; easy to redo</td><td>Extract fields from a PDF, classify a ticket, draft a reply</td><td>Model, verified by rules</td></tr>
  <tr><td>Something changes internally, reversible</td><td>Stage an invoice, assign a ticket, create a draft vendor</td><td>Model, logged, reviewable after the fact</td></tr>
  <tr><td>Something leaves the company or moves money, below a threshold</td><td>Send a standard reply, post a matched invoice under the limit</td><td>Model, with sampling review (e.g. 5% audited weekly)</td></tr>
  <tr><td>Above the threshold, or novel, or affects a relationship</td><td>Post a large invoice, reply to an escalated customer, onboard a new vendor</td><td>Human, presented with the prepared decision</td></tr>
</table>
<p>The threshold is a business rule written by the process owner (amount, customer tier, first-time counterpart, confidence below a bar). It is never the model's own opinion of its confidence alone.</p>

<h2>Design the checkpoint so it gets used</h2>
<p>A checkpoint people skip is worse than none, because it creates the appearance of control. Rules we apply:</p>
<ol>
  <li><strong>Show the decision, not the transcript.</strong> The reviewer sees the invoice fields, the matched PO, the variance, the reason it was flagged and the exact action that will happen on approval. Not a chat log.</li>
  <li><strong>One click, typed outcome.</strong> Approve / Reject / Correct. The outcome is data the orchestrator reads, not a message it interprets.</li>
  <li><strong>In the tool they already use.</strong> Slack, Teams, the helpdesk, the ERP inbox. A new dashboard is a new place to forget.</li>
  <li><strong>Deadline and fallback.</strong> Every request has an owner, a due time and a defined outcome when nobody answers (escalate, or return to requester). Silence must not mean approval.</li>
  <li><strong>Server-side enforcement.</strong> The system that performs the irreversible action checks that an approval exists. The agent cannot talk itself past the gate; neither can a prompt injected through a document.</li>
  <li><strong>Every decision is logged with the reviewer's identity.</strong> This is what an auditor asks for, and it is what lets you widen the safe path later.</li>
</ol>

<h2>Reject is a first-class path</h2>
<p>Most designs handle approval and forget rejection. A rejection should return the item to the requester with the reviewer's note, leave the systems of record untouched, and be visible in metrics. Recurring rejections are the most valuable signal in the whole system: each one is either a rule you have not written yet or a spoke you have not built.</p>

<h2>Shrink the loop deliberately</h2>
<p>Start conservative and widen the automated path on evidence, not on optimism:</p>
<ol>
  <li><strong>Read-only phase.</strong> The system prepares; humans commit everything. You collect the approval log.</li>
  <li><strong>Auto-commit under the threshold.</strong> Only items that pass every rule and fall under the limit go straight through. Measure: straight-through rate, corrections, complaints.</li>
  <li><strong>Raise the threshold or add rules</strong> when the approval log shows reviewers approving a category without changes for a defined period (say 200 items, zero corrections).</li>
  <li><strong>Keep sampling.</strong> Even fully automated categories get a random audit. That is how you notice drift when a vendor changes its invoice format or a model version changes behaviour.</li>
</ol>

<h2>What to measure</h2>
<ul>
  <li>Straight-through rate (no human touch) per category</li>
  <li>Review queue age and time-to-decision</li>
  <li>Approval rate without changes vs. corrected vs. rejected</li>
  <li>Items reversed after auto-commit (the number that must stay near zero)</li>
  <li>Reviewer minutes per item, which is the cost the whole design is trying to reduce</li>
</ul>

<h2>The principle</h2>
<p>People should make decisions, not do work. A well-designed loop presents a person with a prepared, consequential choice a few times a day and keeps everything else moving. If reviewers are reading PDFs or re-keying numbers, the loop is in the wrong place.</p>
""",
 'faq': [
  ('Does a human have to approve every AI action?', 'No. Approvals belong where a wrong action is consequential and hard to reverse: money above a limit, customer-facing messages in sensitive cases, new counterparties. Reads, drafts and low-risk commits run without approval and are audited by sampling.'),
  ('Who sets the approval threshold?', 'The process owner, as a written business rule (amount, customer tier, novelty, confidence bar). The system enforces it server-side; the model cannot lower it.'),
  ('How do we keep reviewers from rubber-stamping?', 'Show a prepared decision rather than a transcript, keep the queue short by automating the safe path, give each request a deadline and fallback, and measure the approve-without-change rate; when it is near 100% for a category, that category is ready to automate.'),
 ],
},
{
 'slug': 'operating-agentic-systems',
 'short': 'Operating agentic systems',
 'kicker': 'Operate & maintain',
 'title': 'Operating agentic systems: what maintenance actually means',
 'desc': 'A live agent team is not a finished project. Models change, APIs change, and the business changes its own rules without telling anyone. This is what ongoing maintenance of an agentic system involves, what to monitor, and what a sensible cadence looks like.',
 'date': '2026-09-22',
 'read': 8,
 'about': ['AI operations', 'Agentic systems', 'LLM evaluation'],
 'keywords': ['agent maintenance', 'LLM operations', 'evals', 'model updates', 'regression testing', 'monitoring agents'],
 'body': '''
<h2>The project ends, the system does not</h2>
<p>Traditional software degrades slowly and visibly: dependencies age, tickets accumulate. An agentic system degrades differently. It keeps returning confident, well-formatted answers while the ground underneath it moves: a supplier changes an invoice layout, a model provider ships a new version, the finance team quietly raises an approval threshold. Nothing throws an exception. The output is simply wrong more often than it was last quarter.</p>
<p>Maintenance is the work of noticing that before anyone else does.</p>

<h2>Four things that change</h2>
<p><strong>The process.</strong> The most common source of drift, and the least technical. Rules change, new exceptions appear, a step moves to another team. The system is still faithfully executing last year's procedure.</p>
<p><strong>The models.</strong> Providers release new versions and retire old ones. A newer model is usually better on average and still different in specifics: it may format an extraction differently, call a tool the old one avoided, or become more cautious in a way that raises the delegation rate.</p>
<p><strong>The systems around it.</strong> APIs change fields, tighten rate limits, deprecate endpoints. A CRM upgrade on a Saturday is an agent incident on Monday.</p>
<p><strong>The data.</strong> Document layouts, naming conventions, volume and seasonality all shift. Retrieval that worked against last year's corpus drifts as the corpus grows.</p>

<h2>Evaluations are the load-bearing part</h2>
<p>Everything else in maintenance depends on having a test set of real cases with known correct outcomes. Without it, every change is a guess and every rollback is an argument.</p>
<p>A working evaluation set has a few properties:</p>
<ul>
  <li><strong>Built from production</strong>, not invented. Real documents, real tickets, real edge cases.</li>
  <li><strong>Includes failures.</strong> Every incident adds a case. This is how a system stops repeating mistakes.</li>
  <li><strong>Covers each skill and each typed error</strong>, including the cases that should escalate.</li>
  <li><strong>Runs cheaply enough to run often</strong>: before every prompt, skill, tool or model change, and on a schedule regardless.</li>
  <li><strong>Reports per category</strong>, not one aggregate score. An average hides the one class of case that broke.</li>
</ul>
<p>Keep it growing. An evaluation set that has not changed in six months is no longer describing the system you are running.</p>

<h2>What to monitor in production</h2>
<p>Four families of signal, all of which should be visible on one page:</p>
<table>
  <thead><tr><th>Signal</th><th>Watch for</th></tr></thead>
  <tbody>
    <tr><td>Outcomes: completed, escalated, failed</td><td>Shift in the mix, week over week</td></tr>
    <tr><td>Delegation rate by reason</td><td>A rising reason means a fixable gap</td></tr>
    <tr><td>Human overrides on approval gates</td><td>A rejected recommendation is a wrong answer caught in time</td></tr>
    <tr><td>Cost and latency per run</td><td>Creeping token spend, retries, slow upstreams</td></tr>
    <tr><td>Tool error rates by type</td><td>Upstream change, credential expiry, new validation rule</td></tr>
  </tbody>
</table>
<p>The override rate deserves special attention: it is the closest thing to a ground-truth accuracy measure a live system produces for free. If reviewers start rejecting more of what the system proposes, something changed, and the evaluation set has not caught it yet.</p>

<h2>Handling a model update</h2>
<p>Model changes are routine, not emergencies, if there is a procedure:</p>
<ol>
  <li>Run the full evaluation set against the new model, per category.</li>
  <li>Compare cost and latency, not just quality: the better model may not be worth it for every role.</li>
  <li>Check tool-calling behaviour specifically, since that is where differences usually show.</li>
  <li>Roll out per agent role rather than everywhere at once. The orchestrator and a narrow specialist do not need the same decision.</li>
  <li>Watch the override and delegation rates for two weeks before calling it done.</li>
</ol>
<p>Keep the previous model configuration available for a rollback. Model routing decided per role, against the evaluation set, is what makes this a controlled change instead of a leap.</p>

<h2>A cadence that works</h2>
<p><strong>Continuously:</strong> monitoring and alerts on failure rates, cost ceilings and stalled runs.</p>
<p><strong>Weekly:</strong> review escalations and overrides from the week; cluster them; turn recurring clusters into a skill change, a tool change or a threshold change.</p>
<p><strong>Monthly:</strong> full evaluation run; review cost per case against the benchmark the system was built to beat; check for upstream API deprecation notices; add the month's incidents to the test set.</p>
<p><strong>Quarterly:</strong> review the process itself with its owner. This is where "we changed that rule in March" surfaces. Review model options, permissions, and whether any part of the system is now doing enough volume to deserve a deterministic pipeline instead of an agent.</p>

<h2>Runbooks and ownership</h2>
<p>Before a system goes live, write down who is called when it misbehaves and what they do first. At minimum: how to pause the agent team without stopping the business process, how to drain the queue of in-flight cases, how to fall back to manual handling, and how to roll back a skill, tool or model change. Agentic systems fail in ways that are unfamiliar to a standard on-call rotation, so the runbook should include examples of what wrongness looks like, not just how to restart a service.</p>

<h2>What maintenance is not</h2>
<p>It is not a support contract that waits for tickets. By the time a user reports that an agent team is getting things wrong, the wrong results have been flowing into a system of record for weeks. Maintenance is the ongoing, scheduled work of measuring a system against reality and adjusting it, which is also the work that makes an agent team an asset rather than an expensive pilot.</p>
''',
 'faq': [
  ('How much maintenance does a live agent team need?', 'Less than building it, and more than zero. Expect a recurring weekly review of escalations and overrides, a monthly evaluation run, and a quarterly session with the process owner, plus reactive work when a model or an upstream API changes. The load falls as the evaluation set matures.'),
  ('Can our own team maintain the system?', 'Usually yes, and it is the right goal. What they need is the evaluation set, the runbook, documented skills with named owners, and monitoring that surfaces the signals above. The part teams most often lack at handover is the habit of adding every incident back into the test set.'),
  ('What is the first sign that an agentic system is drifting?', 'A rising human override rate on approval gates, or a rising delegation rate for one specific reason. Both usually appear before anyone files a complaint, which is why they belong on a dashboard rather than in a monthly report.'),
 ],
},
{
 'slug': 'process-automation-architecture',
 'short': 'Process automation architecture',
 'kicker': 'Process design',
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
