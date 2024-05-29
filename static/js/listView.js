function Edit(id){
    // this Function is for Edit the task
    const token= sessionStorage.getItem('token')
    if (!token) {
        // Validate the token
        console.log('Please Login')
        return
    }
    var anchor = document.createElement("a");
    anchor.href = "/api/editDetails?operation=EDIT&id="+id; // calling the API
    anchor.click();
    
}

function Delete(id) {
    // this Function is used for delete the Task
    const token= sessionStorage.getItem('token')
    if (!token) {
        console.log('Please Login')
        return
    }
    var anchor = document.createElement("a");
    anchor.href = "/api/editDetails?operation=DELETE&id="+id; //Api we are calling
    anchor.click();
}

//Below we are collecting the Variables from editData html page
Task = document.getElementById("Task")
Complexity = document.getElementById("Complexity")
Size = document.getElementById("Size")
typeOfTask = document.getElementById("typeOfTask")
Notes = document.getElementById("Notes")
Estimation = document.getElementById("extimation_time")
Confidence = document.getElementById("confidence_level")
Estimation_range = document.getElementById("extimation_range")

function saveChanges(id) {
    //this function is used for save the edited data
    const token = sessionStorage.getItem('token')
    const reqdata = {
        "id":id,
        "Task": Task.value,
        "Complexity": Complexity.value,
        "Size": Size.value,
        "typeOfTask": typeOfTask.value,
        "Note": Notes.value,
        "Estimation":Estimation.value,
        "Confidence":Confidence.value,
        "Estimation_range":Estimation_range.value
    }
    console.log(reqdata)
    const requestbody = {
        method: 'PATCH',
        headers: {
            'Authorization': token,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(reqdata)
    };
    fetch('/api/editDetails',requestbody).
    then(response=>{
        if(!response.ok){
            throw new Error(response.body)
        }
        return response.json()
    })
    .then(data=>{
        alert("Data Edited Successfully")
        alert(data.update_id)
        ListView()
    })
    .catch(error=>{
        alert(error)
    })
}
