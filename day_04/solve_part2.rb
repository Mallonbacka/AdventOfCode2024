def main()
    file = File.open("input.txt")
    input = file.readlines
    input.map!(&:strip)

    counter = 0
    input_transposed = input.map(&:chars).transpose.map(&:join)
    mas_locations_1 = []

    # First, get the starting coordinates of every MAS
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
      new_string = input[start[1]][start[0]]
      1.step do |i|
        if(input[start[0] + i].nil? || input[start[1] + i].nil?)
            break
        end
        new_string << input[start[1] + i][start[0] + i]
      end
      diagonal_strings.append([start, new_string])
    end
    diagonal_strings.each do |line|
      hits = line[1].enum_for(:scan, /MAS/).map { Regexp.last_match.begin(0) }
      hits += line[1].enum_for(:scan, /SAM/).map { Regexp.last_match.begin(0) }
      hits.each do |i|
        mas_locations_1.append("#{line[0][0] + i + 1},#{line[0][1] + i + 1}")
      end

    end

    mas_locations_2 = []
    start_points = []
    input_reversed = input.map(&:reverse)
    x_length = input_reversed[0].length - 1
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
      new_string = input_reversed[start[1]][start[0]]
      1.step do |i|
        if(input_reversed[start[0] + i].nil? || input_reversed[start[1] + i].nil?)
            break
        end
        new_string << input_reversed[start[1] + i][start[0] + i]
      end
      diagonal_strings.append([start, new_string])
    end
    diagonal_strings.each do |line|
      hits = line[1].enum_for(:scan, /MAS/).map { Regexp.last_match.begin(0) }
      hits += line[1].enum_for(:scan, /SAM/).map { Regexp.last_match.begin(0) }
      hits.each do |i|
        mas_locations_2.append("#{x_length - (line[0][0] + i + 1)},#{line[0][1] + i + 1}")
      end

    end

    puts (mas_locations_1 & mas_locations_2).size
end

main()