function selected_type(obj){
    let parent = obj.parentElement;
    if (obj.className === 'choice-pizza-active') {
        obj.className = 'choice-pizza';
        parent.className = 'pizza_type';
    }else if (obj.className === 'choice-pizza'){
        obj.className = 'choice-pizza-active';
        parent.className = 'pizza_type-selected';
    }
    let selected_pizzas = document.getElementsByClassName("pizza_type-selected");
    console.log(selected_pizzas);
    for (let i = 0; i < selected_pizzas.length; i++){
        console.log(selected_pizzas[i]);
    }
}

function showDescription(obj){
    let img = obj.parentElement.parentElement.getElementsByTagName('img')[0];
    img.style.display = "none";
    let desc = obj.parentElement.parentElement.getElementsByTagName('h4')[0];
    desc.style.display = "";
    desc.style.textAlign = "center";
    desc.style.paddingTop = "60px";
}
function showPhoto(obj){
    let desc = obj.parentElement.parentElement.getElementsByTagName('h4')[0];
    desc.style.display = "none";
    let img = obj.parentElement.parentElement.getElementsByTagName('img')[0];
    img.style.display = "block";
}