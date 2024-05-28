Task = document.getElementById("Task")
Complexity = document.getElementById("Complexity")
Size = document.getElementById("Size")
typeOfTask = document.getElementById("typeOfTask")
Notes = document.getElementById("Notes")
Estimation = document.getElementById("extimation_time")
Confidence = document.getElementById("confidence_level")
Estimation_range = document.getElementById("extimation_range")
const token = sessionStorage.getItem('token')
function logout(){
    if (sessionStorage.getItem('token')){
        sessionStorage.removeItem('token')
        alert('Logout Successfully')
    }
    var anchor = document.createElement("a");
    anchor.href = "/";
    anchor.click();
}

Size.addEventListener('mouseenter', function (event) {
    var inputValue = Task.value;
    const regex = new RegExp(inputValue, 'i');
    fetch('/api/calculate_estimation',{headers:{
        'Authorization': token
    }}).
    then(response=>{
        return response.json()
    })
    .then(data=>{
        if (data.history){
            var items = data.history
            var count1 = 0
            for (let i = 0; i < items.length ; i++){
                if (regex.test(items[i]['Task'])) {
                    if (items[i]['Size'] === '8'){
                        Size.selectedIndex = 1;
                        count1++
                    }
                    if (items[i]['Size'] === '6'){
                        Size.selectedIndex = 2;
                        count1++
                    }
                    if (items[i]['Size'] === '4'){
                        Size.selectedIndex = 3;
                        count1++
                    }
                    if (count1>1){
                        if (items[i]['Complexity'] === Complexity.value){
                            alert('Estimanted complexity is same with current complexity ')
                            count1++
                        }else{
                            alert('Estimated complexity is different from current complexity')
                            count1++
                        }
                        return
                    }
                }
            }
        }else{
            alert(data.message)
        }
    })
})

function reset(){
    Task.value = "";
    Complexity.selectedIndex = 0;
    Size.selectedIndex = 0;
    typeOfTask.selectedIndex = 0;
    Notes.value = "";
    Estimation.value = "";
    Confidence.value = "";
    Estimation_range.value = "";
} 
function Calculate_estimation() {
    if (Task && Complexity && Size && typeOfTask){
        const user_data = {
            "Complexity": Complexity.value,
            "Size": Size.value,
            "typeOfTask": typeOfTask.value,
        };
        const requestData = {
            method: 'POST',
            headers: {
                'Authorization': token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user_data)
        };
        fetch("/api/calculate_estimation",requestData).
        then(response => {
            if (!response.ok) {
                throw new Error('Not Able to fetch the Data')
            } 
            return response.json()
        })
        .then(data =>{
            if(data.message){
                alert(data.message)
                return
            }
            Estimation.value=data.estimated_effort
            Confidence.value=data.confidence_level
            Estimation_range.value=data.estimate_effort_range
        })
        .catch(error=>{
            alert(error)
        })

    } else {
        alert("Fields are empty")
    }
}
function submit_estimation(){
    const reqdata = {
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
        method: 'POST',
        headers: {
            'Authorization': token,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(reqdata)
    };
    fetch('/api/submit_estimation',requestbody).
    then(response=>{
        if(!response.ok){
            throw new Error("Not Able to insert")
        }
        return response.json()
    })
    .then(data=>{
        alert("Data Stored Successfully")
        reset()
    })
    .catch(error=>{
        alert(error)
    })
}