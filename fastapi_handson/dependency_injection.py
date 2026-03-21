from fastapi import FastAPI, Depends

main_fruits_list = ["Apple"]
def main_test():
    return main_fruits_list

app= FastAPI()

@app.get("/fruits")
def check(fruit, ll=Depends(main_test)):
    ll.append(fruit)
    return f"{fruit} is added"
