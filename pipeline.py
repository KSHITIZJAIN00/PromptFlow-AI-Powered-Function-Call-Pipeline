# ai_pipeline_project/pipeline.py
import json
from model_engine import ModelEngine
import functions

class Pipeline:
    def __init__(self):
        self.engine = ModelEngine()

    def run(self, user_query: str):
        plan_json = self.engine.plan_sequence(user_query)
        plan = json.loads(plan_json)

        context = {}
        results = []

        for step in plan:
            fname = step["function"]
            args = step.get("args", {})

            # Replace placeholder references
            for k, v in args.items():
                if isinstance(v, str) and v.startswith("<output_of_"):
                    ref = v.strip("<>").replace("output_of_", "")
                    args[k] = context.get(ref)

            func = getattr(functions, fname, None)
            if not func:
                raise ValueError(f"Unknown function: {fname}")

            output = func(**args)
            context[fname] = output
            results.append({"step": fname, "result": output})

        return {"plan": plan, "results": results}
