@memoized_results = {}

def main()
    file = File.open("input.txt")
    input = file.readlines[0].split(" ")
    input.map!(&:to_i)
    result = input.map do |v|
      process_with_memoize(v, 0)
    end.sum
    puts(result)
end

def process_with_memoize(value, n)
  return 1 if n == 75
  return @memoized_results[[value, n]] if @memoized_results.key?([value, n]) 
  @memoized_results[[value, n]] = begin
    if value == 0
      process_with_memoize(1, n+1)
    elsif value.to_s.length % 2 == 0
      string_value = value.to_s
      length = string_value.length
      return process_with_memoize(string_value[0, length / 2].to_i, n+1) + process_with_memoize(string_value[length/2, length].to_i, n+1)
    else 
      process_with_memoize(value * 2024, n+1)
    end
  end
end

main()