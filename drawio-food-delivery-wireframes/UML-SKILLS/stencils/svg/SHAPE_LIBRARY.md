# UML & Architecture Shape Library

**Version:** 1.0
**Total shapes:** 204
**Categories:** 15

## Summary by delivery

| Delivery | Count |
|----------|-------|
| `annotation` | 16 |
| `generate` | 168 |
| `manual` | 20 |

## Summary by asset type

| Asset type | Count |
|------------|-------|
| `annotation` | 16 |
| `connector` | 45 |
| `marker` | 18 |
| `shape` | 125 |

See [STYLE_GUIDE.md](./STYLE_GUIDE.md) for rendering consistency.

Regenerate: `python scripts/build_inventory.py`

## Basic Geometric Shapes (`basic-geometric`) — 16 shapes

| ID | Name | Visual | Purpose | Delivery | Output |
|----|------|--------|---------|----------|--------|
| `rectangle` | Rectangle | ▭ | Base for classes, components, nodes | `generate` | `shapes/basic-geometric/rectangle.svg` |
| `rounded-rectangle` | Rounded Rectangle | ▭ (rounded) | Activities, actions, use cases | `generate` | `shapes/basic-geometric/rounded-rectangle.svg` |
| `square` | Square | ◻ | Boxes, containers | `generate` | `shapes/basic-geometric/square.svg` |
| `circle` | Circle | ◯ | Interfaces, control points | `generate` | `shapes/basic-geometric/circle.svg` |
| `ellipse` | Ellipse | ◯ (stretched) | Use cases, actors (head) | `generate` | `shapes/basic-geometric/ellipse.svg` |
| `diamond` | Diamond | ◇ | Decisions, branching points | `generate` | `shapes/basic-geometric/diamond.svg` |
| `triangle` | Triangle | ▲ | Directional indicators, signals | `generate` | `shapes/basic-geometric/triangle.svg` |
| `hexagon` | Hexagon | ⬡ | Database notations, signals | `generate` | `shapes/basic-geometric/hexagon.svg` |
| `pentagon` | Pentagon | ⬠ | Send/receive signals | `generate` | `shapes/basic-geometric/pentagon.svg` |
| `cylinder` | Cylinder | ⬢ | Databases, storage | `generate` | `shapes/basic-geometric/cylinder.svg` |
| `folder` | Folder | 📁 | Packages, namespaces | `generate` | `shapes/basic-geometric/folder.svg` |
| `line` | Line | ─── | Connectors, edges | `generate` | `shapes/basic-geometric/line.svg` |
| `arrow` | Arrow | ───▶ | Flow direction, dependencies | `generate` | `shapes/basic-geometric/arrow.svg` |
| `bracket` | Bracket | [ ] | Constraints, stereotypes | `manual` | `shapes/basic-geometric/bracket.svg` |
| `dashed-line` | Dashed Line | ─ ─ ─ | Dependencies, interfaces | `generate` | `shapes/basic-geometric/dashed-line.svg` |
| `dotted-line` | Dotted Line | · · · | Optional relationships | `generate` | `shapes/basic-geometric/dotted-line.svg` |

## UML Class Diagram (`uml-class`) — 16 shapes

| ID | Name | Visual | Purpose | Delivery | Output |
|----|------|--------|---------|----------|--------|
| `class-box` | Class Box | ┌Name├attrs├methods┘ | Core class structure | `generate` | `shapes/uml-class/class-box.svg` |
| `abstract-class` | Abstract Class | ┌*Class*┘ | Abstract classes | `generate` | `shapes/uml-class/abstract-class.svg` |
| `interface-box` | Interface | ┌<<interface>>┘ | Interface definition | `generate` | `shapes/uml-class/interface-box.svg` |
| `enumeration` | Enumeration | ┌<<enumeration>>┘ | Enumerated types | `generate` | `shapes/uml-class/enumeration.svg` |
| `stereotype` | Stereotype | <<stereotype>> | Marking UML elements | `annotation` | `—` |
| `attribute` | Attribute | + name: Type | Class properties | `annotation` | `—` |
| `method` | Method | + method(): ReturnType | Class operations | `annotation` | `—` |
| `visibility-marker` | Visibility Marker | + - # ~ | Access modifiers | `annotation` | `—` |
| `association` | Association | ─────────── | General relationship | `generate` | `shapes/uml-class/association.svg` |
| `aggregation` | Aggregation | ◇─────────── | Has-a relationship | `generate` | `shapes/uml-class/aggregation.svg` |
| `composition` | Composition | ◆─────────── | Part-of relationship | `generate` | `shapes/uml-class/composition.svg` |
| `inheritance` | Inheritance | △─────────── | Is-a relationship | `generate` | `shapes/uml-class/inheritance.svg` |
| `dependency` | Dependency | ─ ─ ─ ─ ▶ | Using relationship | `generate` | `shapes/uml-class/dependency.svg` |
| `realization` | Realization | ─ ─ ─ ─ △ | Implementation | `generate` | `shapes/uml-class/realization.svg` |
| `multiplicity` | Multiplicity | 1, * | Cardinality indicators | `annotation` | `—` |
| `constraint-brace` | Constraint | {constraint} | Business rules | `annotation` | `—` |

## UML Use Case Diagram (`uml-use-case`) — 7 shapes

| ID | Name | Visual | Purpose | Delivery | Output |
|----|------|--------|---------|----------|--------|
| `actor` | Actor | 👤 | User/external system | `generate` | `shapes/uml-use-case/actor.svg` |
| `use-case` | Use Case | (Use Case) | System function | `generate` | `shapes/uml-use-case/use-case.svg` |
| `system-boundary` | System Boundary | ┌ System ┘ | System scope | `generate` | `shapes/uml-use-case/system-boundary.svg` |
| `include-relationship` | Include | ─ ─ ▶ <<include>> | Required functionality | `generate` | `shapes/uml-use-case/include-relationship.svg` |
| `extend-relationship` | Extend | ─ ─ ▶ <<extend>> | Optional functionality | `generate` | `shapes/uml-use-case/extend-relationship.svg` |
| `actor-generalization` | Generalization | △─────────── | Actor inheritance | `generate` | `shapes/uml-use-case/actor-generalization.svg` |
| `actor-head` | Actor Head | ◯ | Actor icon part | `generate` | `shapes/uml-use-case/actor-head.svg` |

## UML Sequence Diagram (`uml-sequence`) — 18 shapes

| ID | Name | Visual | Purpose | Delivery | Output |
|----|------|--------|---------|----------|--------|
| `lifeline` | Lifeline | ┌Obj┘ │ │ │ | Object timeline | `generate` | `shapes/uml-sequence/lifeline.svg` |
| `actor-lifeline` | Actor Lifeline | 👤 │ │ │ | User timeline | `generate` | `shapes/uml-sequence/actor-lifeline.svg` |
| `activation-bar` | Activation Bar | ┌─┐││└─┘ | Execution period | `generate` | `shapes/uml-sequence/activation-bar.svg` |
| `sync-message` | Synchronous Message | ─────▶ | Blocking call | `generate` | `shapes/uml-sequence/sync-message.svg` |
| `async-message` | Asynchronous Message | ─────▷ | Non-blocking call | `generate` | `shapes/uml-sequence/async-message.svg` |
| `return-message` | Return Message | ─ ─ ─ ▶ | Returning value | `generate` | `shapes/uml-sequence/return-message.svg` |
| `self-message` | Self Message | ───┐◄──┘ | Self-call | `generate` | `shapes/uml-sequence/self-message.svg` |
| `create-message` | Create Message | ─ ─ ▶ <<create>> | Object creation | `generate` | `shapes/uml-sequence/create-message.svg` |
| `destroy-message` | Destroy Message | ─────▶ X | Object destruction | `generate` | `shapes/uml-sequence/destroy-message.svg` |
| `combined-fragment` | Combined Fragment | ┌ alt ┘ | Loops, conditions | `generate` | `shapes/uml-sequence/combined-fragment.svg` |
| `alt-fragment` | Alt Fragment | ┌ alt [c] ┘ | Alternative paths | `generate` | `shapes/uml-sequence/alt-fragment.svg` |
| `loop-fragment` | Loop Fragment | ┌ loop ┘ | Repetition | `generate` | `shapes/uml-sequence/loop-fragment.svg` |
| `opt-fragment` | Opt Fragment | ┌ opt ┘ | Optional flow | `generate` | `shapes/uml-sequence/opt-fragment.svg` |
| `par-fragment` | Par Fragment | ┌ par ┘ | Parallel flows | `generate` | `shapes/uml-sequence/par-fragment.svg` |
| `guard` | Guard | [condition] | Conditional logic | `annotation` | `—` |
| `message-number` | Message Number | 1, 1.1, 2 | Message ordering | `annotation` | `—` |
| `interaction-occurrence` | Interaction Occurrence | ref | Reusable interaction | `generate` | `shapes/uml-sequence/interaction-occurrence.svg` |
| `continuation` | Continuation | ┌cont.┘ | Fragment continuation | `generate` | `shapes/uml-sequence/continuation.svg` |

## UML Activity Diagram (`uml-activity`) — 22 shapes

| ID | Name | Visual | Purpose | Delivery | Output |
|----|------|--------|---------|----------|--------|
| `initial-node` | Initial Node | ● | Start of flow | `generate` | `shapes/uml-activity/initial-node.svg` |
| `final-node` | Final Node | ◉ | End of flow | `generate` | `shapes/uml-activity/final-node.svg` |
| `flow-final-node` | Flow Final Node | ⊗ | End of specific flow | `generate` | `shapes/uml-activity/flow-final-node.svg` |
| `action` | Action | ┌ Action ┘ | Single step | `generate` | `shapes/uml-activity/action.svg` |
| `activity` | Activity | ┌<<activity>>┘ | Complex step | `generate` | `shapes/uml-activity/activity.svg` |
| `decision-node` | Decision Node | ◇ | Branching point | `generate` | `shapes/uml-activity/decision-node.svg` |
| `merge-node` | Merge Node | ◇ | Combining paths | `generate` | `shapes/uml-activity/merge-node.svg` |
| `fork-node` | Fork Node | ──── | Parallel splitting | `generate` | `shapes/uml-activity/fork-node.svg` |
| `join-node` | Join Node | ──── | Parallel merging | `generate` | `shapes/uml-activity/join-node.svg` |
| `object-node` | Object Node | ┌ Object ┘ | Data passing | `generate` | `shapes/uml-activity/object-node.svg` |
| `data-store-node` | Data Store Node | ┌<<datastore>>┘ | Data storage | `generate` | `shapes/uml-activity/data-store-node.svg` |
| `send-signal` | Send Signal | ⬠ | Sending signal | `generate` | `shapes/uml-activity/send-signal.svg` |
| `accept-signal` | Accept Signal | ┌──╲│ | Receiving signal | `manual` | `shapes/uml-activity/accept-signal.svg` |
| `accept-time-event` | Accept Time Event | ⏳ | Time-based trigger | `manual` | `shapes/uml-activity/accept-time-event.svg` |
| `interrupting-edge` | Interrupting Edge | ╲╱╲╱╲ | Flow interruption | `generate` | `shapes/uml-activity/interrupting-edge.svg` |
| `swimlane` | Swimlane | ┌ Lane ┘ | Actor/role separation | `generate` | `shapes/uml-activity/swimlane.svg` |
| `activity-partition` | Activity Partition | ┌ Role ┘ | Organization grouping | `generate` | `shapes/uml-activity/activity-partition.svg` |
| `expansion-region` | Expansion Region | ┌─ ─ ─┘ | Multi-element area | `generate` | `shapes/uml-activity/expansion-region.svg` |
| `exception-handler` | Exception Handler | ⚡ | Error handling | `manual` | `shapes/uml-activity/exception-handler.svg` |
| `control-flow` | Control Flow | ─────▶ | Flow direction | `generate` | `shapes/uml-activity/control-flow.svg` |
| `object-flow` | Object Flow | ─ ─ ─ ▶ | Object movement | `generate` | `shapes/uml-activity/object-flow.svg` |
| `interrupting-flow` | Interrupting Flow | ─────▶⚡ | Flow interruption | `manual` | `shapes/uml-activity/interrupting-flow.svg` |

## UML State Machine Diagram (`uml-state-machine`) — 18 shapes

| ID | Name | Visual | Purpose | Delivery | Output |
|----|------|--------|---------|----------|--------|
| `state` | State | ┌ State ┘ | Object state | `generate` | `shapes/uml-state-machine/state.svg` |
| `sm-initial-state` | Initial State | ● | Starting point | `generate` | `shapes/uml-state-machine/sm-initial-state.svg` |
| `sm-final-state` | Final State | ◉ | End point | `generate` | `shapes/uml-state-machine/sm-final-state.svg` |
| `choice-pseudostate` | Choice Pseudo-state | ◇ | Conditional branching | `generate` | `shapes/uml-state-machine/choice-pseudostate.svg` |
| `fork-pseudostate` | Fork Pseudo-state | ──── | Parallel splitting | `generate` | `shapes/uml-state-machine/fork-pseudostate.svg` |
| `join-pseudostate` | Join Pseudo-state | ──── | Parallel merging | `generate` | `shapes/uml-state-machine/join-pseudostate.svg` |
| `deep-history` | Deep History | H* | History deep | `generate` | `shapes/uml-state-machine/deep-history.svg` |
| `shallow-history` | Shallow History | H | History shallow | `generate` | `shapes/uml-state-machine/shallow-history.svg` |
| `entry-point` | Entry Point | ●→ | Entry into composite | `manual` | `shapes/uml-state-machine/entry-point.svg` |
| `exit-point` | Exit Point | ● | Exit from composite | `manual` | `shapes/uml-state-machine/exit-point.svg` |
| `composite-state` | Composite State | ┌ State ┌─┐ ┘ | Nested states | `generate` | `shapes/uml-state-machine/composite-state.svg` |
| `submachine-state` | Submachine State | ┌ State ref ┘ | Reusable state | `generate` | `shapes/uml-state-machine/submachine-state.svg` |
| `transition` | Transition | ────▶ trigger | State change | `generate` | `shapes/uml-state-machine/transition.svg` |
| `internal-transition` | Internal Transition | ───┐◄──┘ | Self-transition | `generate` | `shapes/uml-state-machine/internal-transition.svg` |
| `completion-transition` | Completion Transition | ─────▶ | Automatic transition | `generate` | `shapes/uml-state-machine/completion-transition.svg` |
| `transition-event` | Event | event() | Triggering event | `annotation` | `—` |
| `transition-guard` | Transition Guard | [condition] | Condition for transition | `annotation` | `—` |
| `transition-action` | Transition Action | / action | Activity on transition | `annotation` | `—` |

## UML Component & Deployment (`uml-component-deployment`) — 12 shapes

| ID | Name | Visual | Purpose | Delivery | Output |
|----|------|--------|---------|----------|--------|
| `component` | Component | ┌<<component>>┘ | System component | `generate` | `shapes/uml-component-deployment/component.svg` |
| `component-lollipop` | Component with Lollipop | ┌───○ | Provided interface | `generate` | `shapes/uml-component-deployment/component-lollipop.svg` |
| `component-socket` | Component with Socket | ┌───( | Required interface | `generate` | `shapes/uml-component-deployment/component-socket.svg` |
| `interface-provided` | Interface (Provided) | ○ | Provided interface | `generate` | `shapes/uml-component-deployment/interface-provided.svg` |
| `interface-required` | Interface (Required) | ( | Required interface | `generate` | `shapes/uml-component-deployment/interface-required.svg` |
| `port` | Port | □ | Interaction point | `generate` | `shapes/uml-component-deployment/port.svg` |
| `artifact` | Artifact | ┌<<artifact>>┘ | Deployment artifact | `generate` | `shapes/uml-component-deployment/artifact.svg` |
| `node` | Node | ┌ Node ┘ | Physical resource | `generate` | `shapes/uml-component-deployment/node.svg` |
| `device` | Device | ┌<<device>>┘ | Hardware device | `generate` | `shapes/uml-component-deployment/device.svg` |
| `execution-environment` | Execution Environment | ┌<<EE>>┘ | Software environment | `generate` | `shapes/uml-component-deployment/execution-environment.svg` |
| `deployment-relationship` | Deployment | ─ ─ ▶ <<deploy>> | Deployment relationship | `generate` | `shapes/uml-component-deployment/deployment-relationship.svg` |
| `manifest-relationship` | Manifest | ─ ─ ▶ <<manifest>> | Artifact manifestation | `generate` | `shapes/uml-component-deployment/manifest-relationship.svg` |

## UML Package & Organizational (`uml-package`) — 7 shapes

| ID | Name | Visual | Purpose | Delivery | Output |
|----|------|--------|---------|----------|--------|
| `package` | Package | ┌ Package ┘ | Grouping element | `generate` | `shapes/uml-package/package.svg` |
| `package-stereotype` | Package with Stereotype | ┌<<st>> Package┘ | Typed package | `generate` | `shapes/uml-package/package-stereotype.svg` |
| `model` | Model | ┌<<model>>┘ | Model grouping | `generate` | `shapes/uml-package/model.svg` |
| `subsystem` | Subsystem | ┌<<subsystem>>┘ | Subsystem grouping | `generate` | `shapes/uml-package/subsystem.svg` |
| `profile` | Profile | ┌<<profile>>┘ | Stereotype definition | `generate` | `shapes/uml-package/profile.svg` |
| `package-import` | Package Import | ─ ─ ▶ <<import>> | Package dependency | `generate` | `shapes/uml-package/package-import.svg` |
| `package-merge` | Package Merge | ─ ─ ▶ <<merge>> | Package combination | `generate` | `shapes/uml-package/package-merge.svg` |

## Architecture Diagram (`architecture`) — 20 shapes

| ID | Name | Visual | Purpose | Delivery | Output |
|----|------|--------|---------|----------|--------|
| `microservice` | Microservice | ┌<<ms>> Service┘ | Microservice | `generate` | `shapes/architecture/microservice.svg` |
| `api-gateway` | API Gateway | ┌<<gateway>> API┘ | API gateway | `generate` | `shapes/architecture/api-gateway.svg` |
| `database` | Database | ⬢ | Database | `generate` | `shapes/architecture/database.svg` |
| `cache` | Cache | ┌ ⚡ Cache ┘ | Cache layer | `generate` | `shapes/architecture/cache.svg` |
| `message-queue` | Message Queue | ┌<<queue>>┘ | Message queue | `generate` | `shapes/architecture/message-queue.svg` |
| `load-balancer` | Load Balancer | ┌<<lb>> LB┘ | Load balancer | `generate` | `shapes/architecture/load-balancer.svg` |
| `firewall` | Firewall | ┌<<fw>> FW┘ | Firewall | `generate` | `shapes/architecture/firewall.svg` |
| `storage` | Storage | ┌<<storage>>┘ | Object storage | `generate` | `shapes/architecture/storage.svg` |
| `container` | Container | ┌<<container>>┘ | Container | `generate` | `shapes/architecture/container.svg` |
| `pod` | Pod | ┌<<pod>>┘ | Kubernetes pod | `generate` | `shapes/architecture/pod.svg` |
| `k8s-service` | Service | ┌<<service>>┘ | Kubernetes service | `generate` | `shapes/architecture/k8s-service.svg` |
| `ingress` | Ingress | ┌<<ingress>>┘ | Kubernetes ingress | `generate` | `shapes/architecture/ingress.svg` |
| `configmap` | ConfigMap | ┌<<config>>┘ | Kubernetes config | `generate` | `shapes/architecture/configmap.svg` |
| `secret` | Secret | ┌<<secret>>┘ | Kubernetes secret | `generate` | `shapes/architecture/secret.svg` |
| `persistent-volume` | Persistent Volume | ┌<<pv>>┘ | Storage volume | `generate` | `shapes/architecture/persistent-volume.svg` |
| `namespace` | Namespace | ┌<<ns>>┘ | Kubernetes namespace | `generate` | `shapes/architecture/namespace.svg` |
| `consumer` | Consumer | ┌<<consumer>>┘ | Event consumer | `generate` | `shapes/architecture/consumer.svg` |
| `producer` | Producer | ┌<<producer>>┘ | Event producer | `generate` | `shapes/architecture/producer.svg` |
| `broker` | Broker | ┌<<broker>>┘ | Message broker | `generate` | `shapes/architecture/broker.svg` |
| `topic` | Topic | ┌<<topic>>┘ | Kafka topic | `generate` | `shapes/architecture/topic.svg` |

## Data & Database (`data-database`) — 8 shapes

| ID | Name | Visual | Purpose | Delivery | Output |
|----|------|--------|---------|----------|--------|
| `table` | Table | ┌ Table ┘ | Database table | `generate` | `shapes/data-database/table.svg` |
| `view-db` | View | ┌<<view>>┘ | Database view | `generate` | `shapes/data-database/view-db.svg` |
| `stored-procedure` | Stored Procedure | ┌<<sp>>┘ | Stored procedure | `generate` | `shapes/data-database/stored-procedure.svg` |
| `index-db` | Index | ┌<<index>>┘ | Database index | `generate` | `shapes/data-database/index-db.svg` |
| `primary-key` | Primary Key | id PK | Primary key | `annotation` | `—` |
| `foreign-key` | Foreign Key | id FK | Foreign key | `annotation` | `—` |
| `table-relationship` | Relationship | 1 ─── * | Table relationship | `generate` | `shapes/data-database/table-relationship.svg` |
| `er-entity` | Entity | ┌ Entity ┘ | ER entity | `generate` | `shapes/data-database/er-entity.svg` |

## Cloud Architecture (`cloud-architecture`) — 16 shapes

| ID | Name | Visual | Purpose | Delivery | Output |
|----|------|--------|---------|----------|--------|
| `aws-ec2` | AWS EC2 | EC2 | AWS compute | `generate` | `shapes/cloud-architecture/aws-ec2.svg` |
| `aws-s3` | AWS S3 | S3 | AWS storage | `generate` | `shapes/cloud-architecture/aws-s3.svg` |
| `aws-rds` | AWS RDS | RDS | AWS database | `generate` | `shapes/cloud-architecture/aws-rds.svg` |
| `aws-lambda` | AWS Lambda | λ | AWS serverless | `generate` | `shapes/cloud-architecture/aws-lambda.svg` |
| `aws-api-gateway` | AWS API Gateway | APIG | AWS API gateway | `generate` | `shapes/cloud-architecture/aws-api-gateway.svg` |
| `aws-vpc` | AWS VPC | VPC | AWS network | `generate` | `shapes/cloud-architecture/aws-vpc.svg` |
| `azure-vm` | Azure VM | VM | Azure compute | `manual` | `shapes/cloud-architecture/azure-vm.svg` |
| `azure-blob` | Azure Blob | Blob | Azure storage | `manual` | `shapes/cloud-architecture/azure-blob.svg` |
| `azure-sql` | Azure SQL | SQL | Azure database | `manual` | `shapes/cloud-architecture/azure-sql.svg` |
| `azure-functions` | Azure Functions | ⚡ | Azure serverless | `manual` | `shapes/cloud-architecture/azure-functions.svg` |
| `gcp-compute` | GCP Compute Engine | GCE | GCP compute | `manual` | `shapes/cloud-architecture/gcp-compute.svg` |
| `gcp-storage` | GCP Cloud Storage | GCS | GCP storage | `manual` | `shapes/cloud-architecture/gcp-storage.svg` |
| `gcp-bigquery` | GCP BigQuery | BQ | GCP data warehouse | `manual` | `shapes/cloud-architecture/gcp-bigquery.svg` |
| `cloud-region` | Cloud Region | us-east-1 | Cloud region | `generate` | `shapes/cloud-architecture/cloud-region.svg` |
| `cloud-az` | Cloud Availability Zone | AZ-A | Availability zone | `generate` | `shapes/cloud-architecture/cloud-az.svg` |
| `cloud-generic` | Cloud Generic | Cloud | Fallback cloud node | `generate` | `shapes/cloud-architecture/cloud-generic.svg` |

## Infrastructure & Network (`infrastructure-network`) — 9 shapes

| ID | Name | Visual | Purpose | Delivery | Output |
|----|------|--------|---------|----------|--------|
| `server` | Server | Server | Physical server | `generate` | `shapes/infrastructure-network/server.svg` |
| `switch` | Switch | Switch | Network switch | `generate` | `shapes/infrastructure-network/switch.svg` |
| `router` | Router | Router | Network router | `generate` | `shapes/infrastructure-network/router.svg` |
| `firewall-network` | Firewall | FW | Network firewall | `generate` | `shapes/infrastructure-network/firewall-network.svg` |
| `load-balancer-network` | Load Balancer | LB | Network load balancer | `generate` | `shapes/infrastructure-network/load-balancer-network.svg` |
| `vpn` | VPN | VPN | VPN gateway | `generate` | `shapes/infrastructure-network/vpn.svg` |
| `internet` | Internet | ☁ | External network | `generate` | `shapes/infrastructure-network/internet.svg` |
| `dmz` | DMZ | DMZ | Network DMZ | `generate` | `shapes/infrastructure-network/dmz.svg` |
| `subnet` | Subnet | 10.0.1.0/24 | Network subnet | `generate` | `shapes/infrastructure-network/subnet.svg` |

## Process & Flow (`process-flow`) — 11 shapes

| ID | Name | Visual | Purpose | Delivery | Output |
|----|------|--------|---------|----------|--------|
| `process` | Process | Process | Standard process | `generate` | `shapes/process-flow/process.svg` |
| `flow-start` | Start | ● | Process start | `generate` | `shapes/process-flow/flow-start.svg` |
| `flow-end` | End | ◉ | Process end | `generate` | `shapes/process-flow/flow-end.svg` |
| `flow-decision` | Decision | ◇ | Decision point | `generate` | `shapes/process-flow/flow-decision.svg` |
| `document` | Document | Document | Document output | `manual` | `shapes/process-flow/document.svg` |
| `data-parallelogram` | Data | Data | Data input | `manual` | `shapes/process-flow/data-parallelogram.svg` |
| `predefined-process` | Predefined Process | Process | Subroutine | `generate` | `shapes/process-flow/predefined-process.svg` |
| `manual-input` | Manual Input | Manual | Manual entry | `manual` | `shapes/process-flow/manual-input.svg` |
| `display` | Display | Display | Screen output | `manual` | `shapes/process-flow/display.svg` |
| `manual-operation` | Manual Operation | Manual | Manual task | `manual` | `shapes/process-flow/manual-operation.svg` |
| `off-page-connector` | Off-page Connector | ⬠ | Connector to another page | `generate` | `shapes/process-flow/off-page-connector.svg` |

## Connector & Line Types (`connector-line`) — 14 shapes

| ID | Name | Visual | Purpose | Delivery | Output |
|----|------|--------|---------|----------|--------|
| `line-solid` | Solid Line | ─────────── | Association, flow | `generate` | `shapes/connector-line/line-solid.svg` |
| `line-dashed` | Dashed Line | ─ ─ ─ ─ ─ | Dependency, optional | `generate` | `shapes/connector-line/line-dashed.svg` |
| `line-dotted` | Dotted Line | · · · · · | Weak relationship | `generate` | `shapes/connector-line/line-dotted.svg` |
| `arrow-solid` | Solid Arrow | ───────────▶ | Synchronous flow | `generate` | `shapes/connector-line/arrow-solid.svg` |
| `arrow-open` | Open Arrow | ───────────▷ | Asynchronous flow | `generate` | `shapes/connector-line/arrow-open.svg` |
| `arrow-dashed` | Dashed Arrow | ─ ─ ─ ─ ▶ | Dependency | `generate` | `shapes/connector-line/arrow-dashed.svg` |
| `arrow-double` | Double-headed Arrow | ◀──────────▶ | Bi-directional | `generate` | `shapes/connector-line/arrow-double.svg` |
| `arrow-hollow-triangle` | Solid Triangle Arrow | ───────────△ | Inheritance | `generate` | `shapes/connector-line/arrow-hollow-triangle.svg` |
| `arrow-dashed-triangle` | Dashed Triangle Arrow | ─ ─ ─ ─ △ | Realization | `generate` | `shapes/connector-line/arrow-dashed-triangle.svg` |
| `diamond-hollow-end` | Hollow Diamond | ◇─────────── | Aggregation | `generate` | `shapes/connector-line/diamond-hollow-end.svg` |
| `diamond-filled-end` | Filled Diamond | ◆─────────── | Composition | `generate` | `shapes/connector-line/diamond-filled-end.svg` |
| `self-loop` | Self-loop | ───┐◄──┘ | Self-reference | `generate` | `shapes/connector-line/self-loop.svg` |
| `zigzag-line` | Zigzag Line | ╲╱╲╱╲ | Interrupting flow | `generate` | `shapes/connector-line/zigzag-line.svg` |
| `bend-point` | Bend Point | ● | Connector control point | `generate` | `shapes/connector-line/bend-point.svg` |

## Miscellaneous (`miscellaneous`) — 10 shapes

| ID | Name | Visual | Purpose | Delivery | Output |
|----|------|--------|---------|----------|--------|
| `note` | Note | Note | Comments | `manual` | `shapes/miscellaneous/note.svg` |
| `constraint-text` | Constraint | {constraint} | Limitation | `annotation` | `—` |
| `tag` | Tag | Tag | Metadata | `generate` | `shapes/miscellaneous/tag.svg` |
| `legend` | Legend | Legend | Diagram legend | `generate` | `shapes/miscellaneous/legend.svg` |
| `title-block` | Title Block | Project | Document header | `generate` | `shapes/miscellaneous/title-block.svg` |
| `timeline` | Timeline | ──────── | Timeline | `generate` | `shapes/miscellaneous/timeline.svg` |
| `milestone` | Milestone | ◆ | Milestone | `generate` | `shapes/miscellaneous/milestone.svg` |
| `phase` | Phase | Phase 1 | Project phase | `generate` | `shapes/miscellaneous/phase.svg` |
| `sequence-number` | Number | 1, 2, 3 | Sequence numbers | `annotation` | `—` |
| `condition-text` | Condition | [condition] | Guard condition | `annotation` | `—` |
