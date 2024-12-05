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

let fixedUpdates = []
let answer = 0

updates.forEach(update => {
    let workingUpdate = update.slice()

    let isOriginallyValid = true

    for( let i = 0; i < workingUpdate.length; i++){
        const prevs = workingUpdate.slice(0, i)
        const current = workingUpdate[i]
        const coming = workingUpdate.slice(i + 1) 

        if(ordering_rules[current] && ordering_rules[current].filter(x => prevs.includes(x)).length > 0){
            isOriginallyValid = false
            const notAllowedBefore = ordering_rules[current].filter(x => prevs.includes(x))

            let targetIndex = Math.min(...notAllowedBefore.map(x => {
                return workingUpdate.indexOf(x)
            }))

            rearrangedUpdate = workingUpdate.slice(0, targetIndex)
                .concat([current])
                .concat(workingUpdate.slice(targetIndex, i))
                .concat(coming)

            workingUpdate = rearrangedUpdate
        }
    }

    if (!isOriginallyValid){
        fixedUpdates = fixedUpdates.concat([rearrangedUpdate])
        answer += parseInt(rearrangedUpdate[Math.floor(rearrangedUpdate.length / 2)])
    }
})

console.log(answer)
