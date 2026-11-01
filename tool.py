from datetime import datetime
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

Tools=[
    {
        "type":"function",
        "name":"get_current_time",
        "description":"Get the current date and time in the format YYYY-MM-DD HH:MM:SS",
        "parameters":{
            "type":"object",
            "properties":{},
            
        },
        #write down all parameters that are required for this function to work.
        "required":[]
    }
]

FUNCTION_NAME_TO_FUNCTION_MAP={
    "get_current_time":get_current_time
}
