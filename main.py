from pipeline import Pipeline
import json

def main():
    queries = [
        "Get invoices for March, summarize them, and email me the report.",
        "Create a calendar event called 'Meeting' on 2025-07-01 at 09:00.",
        "Generate invoice summary for June and save to a file."
    ]

    pipeline = Pipeline()
    for i, query in enumerate(queries, 1):
        print(f"\n=== Query {i}: {query} ===")
        result = pipeline.run(query)
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
