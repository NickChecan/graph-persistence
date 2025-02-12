# graph-persistence
This is a very simple project that shows the setup of a memory mechanism
for a human-in-the-loop system. 

```mermaid
%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph TD;
	__start__([<p>__start__</p>]):::first
	step_1(step_1)
	human_feedback(human_feedback<hr/><small><em>__interrupt = before</em></small>)
	step_3(step_3)
	__end__([<p>__end__</p>]):::last
	__start__ --> step_1;
	human_feedback --> step_3;
	step_1 --> human_feedback;
	step_3 --> __end__;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
```

## Utilities

```sh
poetry add langgraph langchain-community python-dotenv black isort grandalf
```