X_LIMIT = 101
Y_LIMIT = 103

NEIGHBOR_THRESHOLD = 0.75

class Solver
  def main()
      file = File.open("input.txt")
      input = file.readlines
      @robots = input.map do |robot_string|
        input_values = robot_string.scan(/p=(\d+),(\d+) v=(-{0,1}\d+),(-{0,1}\d+)/)
        Robot.new(*input_values[0])
      end
      10402.times do |n|
        @robots.map(&:step)
        if(@robots.map{ |r| r.has_neighbor?(@robots) ? 1 : 0 }.reduce(:+).to_f / @robots.size) > NEIGHBOR_THRESHOLD
          # Write map for manual checking in case there are multiple
          # Edit: There was just the one, so interrupting and returning the number would work too
          write_map("results/" + (n + 1).to_s.rjust(6, '0'))
        end
      end
  end

  def write_map(filename)
    File.open("#{filename}.pbm", 'w') do |file| 
      file.write("P1\n") 
      file.write("#{X_LIMIT} #{Y_LIMIT}\n")
      Y_LIMIT.times do |y|
        X_LIMIT.times do |x|
          if(@robots.find{ |r| r.to_s == "Robot at #{x}, #{y}" })
            file.write("1")
          else
            file.write("0")
          end
        end
        file.write("\n")
      end 
    end
  end
end

class Robot
  def initialize(start_x, start_y, step_x, step_y)
    @location = Point.new(start_x.to_i, start_y.to_i)
    @start_location = @location
    @step_x = step_x.to_i
    @step_y = step_y.to_i
  end

  def current_location
    @location
  end

  def quadrant
    @location.quadrant
  end

  def at_start_position
    @location == @start_location
  end

  def to_s
    "Robot at #{@location}"
  end

  def step
    @location = @location.moved_by(@step_x, @step_y)
  end

  def has_neighbor?(all_robots)
    all_robots.any?{ |r| r.distance_from(self.current_location) <= 2 && r.distance_from(self.current_location) > 0 }
  end

  def distance_from(other)
    (self.current_location.x - other.x).abs + (self.current_location.y - other.y).abs
  end
end

class Point
  def initialize(x, y)
    @current_x = x
    @current_y = y
  end

  def x
    @current_x
  end

  def y
    @current_y
  end

  def moved_by(step_x, step_y)
    Point.new((@current_x + step_x) % X_LIMIT, (@current_y + step_y) % Y_LIMIT)
  end

  def ==(other)
    x == other.x && y == other.y
  end

  def quadrant
    if(x < X_LIMIT / 2)
      if (y < Y_LIMIT / 2)
        return "NW"
      elsif (y > Y_LIMIT / 2)
        return "SW"
      end
    elsif(x > X_LIMIT / 2)
      if (y < Y_LIMIT / 2)
        return "NE"
      elsif (y > Y_LIMIT / 2)
        return "SE"
      end
    end
    return nil
  end

  def to_s
    "#{x}, #{y}"
  end
end

Solver.new.main()