from .query_understanding import understand_query
from .intent_classifier import classify_intent
from .task_classifier import classify_task



def route_query(query:str)->dict:


    # Step 1
    query_result = understand_query(query)


    if not query_result["valid"]:

        return query_result



    # Step 2

    intent_result = classify_intent(query)



    if not intent_result["valid"]:

        return {

            "valid":False,

            "stage":"intent_classifier",

            "message":
            intent_result["message"]

        }



    # Step 3

    task_result = classify_task(

        query,

        intent_result["intent"]

    )



    if not task_result["valid"]:

        return {

            "valid":False,

            "stage":"task_classifier",

            "message":
            task_result["message"]

        }




    return {


        "valid":True,


        "query":query,


        "intent":
        intent_result["intent"],


        "query_type":
        intent_result["query_type"],


        "task":
        task_result["task"],


        "model":
        task_result["model"],


        "intent_reason":
        intent_result["reason"],


        "task_reason":
        task_result["reason"],


        "message":
        "Global routing completed successfully."

    }