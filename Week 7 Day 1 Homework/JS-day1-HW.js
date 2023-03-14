//==================Exercise #1 ==========//
/*Write a function that takes in the string and the list of dog names, loops through 
the list and checks that the current name is in the string passed in. The output should be:
`Matched ${dog_name}` if name is in the string, if its not a match console.log "No Match"
*/

// Test values
let dog_string = "Hello Max, my name is Dog, and I have purple eyes!";
let dog_names = ["Max","HAS","PuRple","dog"];

function findWords(dog_string, name_array){
    // Use regex to sort through string and output to an arrary
    let dog_array = dog_string.toLowerCase().match(/\b[\w']+\b/g); 
    
    // Loop through array of names then check against array of strings
    for(let name of name_array){
        for(let word of dog_array) {
            if (name.toLowerCase() == word) {
                console.log(`Matched ${name}`)
            } else {
                console.log(`No Match`)
            }
        }
    }
}
// Test it bb
findWords(dog_string, dog_names);


//============Exercise #2 ============//
/*Write a function that takes in an array and removes every even index with a splice,
and replaces it with the string "even index" */

// Test value
let arr = ["Max","Baseball","Reboot","Goku","Trucks","Rodger"];

function replaceEvens(a_arr){
    // Grab index number of array
    for(let i in a_arr){
        // Check if index is even using module, replace even numbered indices w/ string
        if (i % 2 == 0) {
            console.log(a_arr.splice(i, 1, "even index"))
        }
    }
    console.log(a_arr)
}

// Test it bb
replaceEvens(arr)

//Expected output
//Given arr == ["Max","Baseball","Reboot","Goku","Trucks","Rodger"]
//Output arr == ["even index","Baseball","even index","Goku","even index","Rodger"]