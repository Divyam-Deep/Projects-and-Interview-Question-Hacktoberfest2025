// ====================================
// DICE ROLLER (Node.js Console Version)
// ====================================

// Import the readline module to take input from the console
const readline = require("readline");

// Create an interface to read input and write output in the console
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

// Function to roll the dice
function rollDice() {
  // Generate a random number between 1 and 6
  const diceValue = Math.floor(Math.random() * 6) + 1;
  console.log(`You rolled a: ${diceValue}`);
}

// Function to ask the user if they want to roll again
function askToRollAgain() {
  rl.question("Do you want to roll the dice? (yes/no): ", (answer) => {
    const userInput = answer.trim().toLowerCase(); // remove spaces and make lowercase

    if (userInput === "yes" || userInput === "y") {
      rollDice(); // roll the dice
      askToRollAgain(); // ask again
    } else if (userInput === "no" || userInput === "n") {
      console.log("Thanks for playing! Goodbye!");
      rl.close(); // close the input interface
    } else {
      console.log("Please enter 'yes' or 'no'.");
      askToRollAgain(); // ask again if invalid input
    }
  });
}

// Start the game
console.log("Welcome to the Dice Roller Game!");
askToRollAgain();