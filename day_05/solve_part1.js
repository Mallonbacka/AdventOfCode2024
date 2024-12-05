var fs = require('fs');
var lines = fs.readFileSync('input.txt').toString().split("\n");
let ordering_rules = {}
let ordering_rules_reverse = {}
let updates = []
for(i in lines) {
    if (lines[i].includes("|")){
        const rule_parts = lines[i].trim().split("|")
        ordering_rules[rule_parts[0]] = (ordering_rules[rule_parts[0]] || []).concat([rule_parts[1]])
        ordering_rules_reverse[rule_parts[1]] = (ordering_rules_reverse[rule_parts[1]] || []).concat([rule_parts[0]])
    }else if (lines[i].includes(",")){
        updates = updates.concat([lines[i].trim().split(",")])
    }
}

let answer = 0

updates.forEach(update => {
    let prevs = []
    let current = update[0]
    let coming = update.slice(1)

    let isValid = true

    while(coming.length > 0){

        prevs = prevs.concat([current])
        current = coming[0]
        coming = coming.slice(1) 

        // These are not allowed in coming
        if(ordering_rules_reverse[current] && ordering_rules_reverse[current].filter(x => coming.includes(x)).length > 0){
            isValid = false
            break
        }

        if(ordering_rules[current] && ordering_rules[current].filter(x => prevs.includes(x)).length > 0){
            isValid = false
            break
        }
    }

    if (isValid){
        console.log(update)
        console.log(Math.floor(update.length / 2))
        answer += parseInt(update[Math.floor(update.length / 2)])
    }
})

console.log(answer)
