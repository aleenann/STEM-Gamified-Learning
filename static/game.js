let score = 0;

function startGame(){

let answer = prompt("What is 10 + 5 ?");

if(answer == 15){

score += 10;
alert("Correct! +10 points");

}

else{

alert("Wrong answer");

}

document.getElementById("score").innerText = score;

}