def main()
    file = File.open("input.txt")
    input = file.readlines[0].split(" ")
    input.map!(&:to_i)
    25.times do |n|
      puts n
      input = input.flat_map do |v|
        process_rules(v)
      end
    end
    puts(input.length)
end

def process_rules(value)
  if(value == 0)
    return 1
  elsif(value.to_s.length % 2 == 0)
    string_value = value.to_s
    length = string_value.length
    return [string_value[0, length / 2].to_i, string_value[length/2, length].to_i]
  else
    return value * 2024
  end
end

main()