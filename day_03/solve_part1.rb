def main()
    file = File.open("input.txt")
    input = file.read
    pattern = /mul\([0-9]{1,3},[0-9]{1,3}\)/
    results = input.scan(pattern)
    total = 0
    results.each do |result|
        values = result.sub("mul(", "").sub(")", "").split(",").map(&:to_i)
        total += values[0] * values[1]
    end
    puts(total)
end

main()