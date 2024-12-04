def main()
    file = File.open("input.txt")
    input = file.readlines
    input.map!(&:strip)

    counter = 0

    # Horizontal
    input.each do |line|
      puts line
      counter += line.scan(/XMAS/).size
      counter += line.scan(/SAMX/).size
    end

    # Vertical
    input_transposed = input.map(&:chars).transpose.map(&:join)
    input_transposed.each do |line|
      counter += line.scan(/XMAS/).size
      counter += line.scan(/SAMX/).size
    end

    # Diagonal, top-left to bottom right
    start_points = []
    # Top row
    input[0].length.times do |i|
      start_points.append([i, 0])
    end
    # First column
    input_transposed[0].length.times do |i|
        start_points.append([0, i])
    end

    diagonal_strings = []
    start_points.uniq.each do |start|
      new_string = input[start[0]][start[1]]
      1.step do |i|
        if(input[start[0] + i].nil? || input[start[1] + i].nil?)
            break
        end
        new_string << input[start[0] + i][start[1] + i]
      end
      diagonal_strings.append(new_string)
    end
    diagonal_strings.each do |line|
      counter += line.scan(/XMAS/).size
      counter += line.scan(/SAMX/).size
    end

    # Diagonal, top-right to bottom left 
    start_points = []
    input_reversed = input.map(&:reverse)
    # Top row
    input_reversed[0].length.times do |i|
      start_points.append([i, 0])
    end
    # First column
    input_transposed[0].length.times do |i|
        start_points.append([0, i])
    end

    diagonal_strings = []
    start_points.uniq.each do |start|
      new_string = input_reversed[start[0]][start[1]]
      1.step do |i|
        if(input_reversed[start[0] + i].nil? || input_reversed[start[1] + i].nil?)
            break
        end
        new_string << input_reversed[start[0] + i][start[1] + i]
      end
      diagonal_strings.append(new_string)
    end
    diagonal_strings.each do |line|
      counter += line.scan(/XMAS/).size
      counter += line.scan(/SAMX/).size
    end
    puts counter
end

main()