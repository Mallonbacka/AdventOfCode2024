def main()
    file = File.open("input.txt")
    input = file.read
    pattern = /mul\([0-9]{1,3},[0-9]{1,3}\)/
    
    donts = input.enum_for(:scan, /don't\(\)/).map { Regexp.last_match.begin(0) }
    dos = input.enum_for(:scan, /do\(\)/).map { Regexp.last_match.begin(0) }

    puts input  
    donts.each do |dont_i|
        next_do = dos.filter{|x| x > dont_i }.first || input.length - 1
        input[dont_i..next_do] = 'X' * (next_do - dont_i + 1)
    end

    puts input  
    results = input.scan(pattern)
    total = 0
    results.each do |result|
        values = result.sub("mul(", "").sub(")", "").split(",").map(&:to_i)
        total += values[0] * values[1]
    end
    puts(total)
end

main()