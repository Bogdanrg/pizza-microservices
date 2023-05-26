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

function removePizza(obj){
    let pizza = obj.parentElement.parentElement;
    pizza.style.display="none";
}