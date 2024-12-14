X_LIMIT = 101
Y_LIMIT = 103

class Solver
  def main()
      file = File.open("input.txt")
      input = file.readlines
      @robots = input.map do |robot_string|
        input_values = robot_string.scan(/p=(\d+),(\d+) v=(-{0,1}\d+),(-{0,1}\d+)/)
        Robot.new(*input_values[0])
      end
      100.times do 
        @robots.map(&:step)
      end
      puts(@robots.group_by(&:quadrant).except(nil).values.map(&:length).inject(:*))
  end

  def print_map
    Y_LIMIT.times do |y|
      X_LIMIT.times do |x|
        if(@robots.find{ |r| r.to_s == "Robot at #{x}, #{y}" })
          print("1")
        else
          print(".")
        end
      end
      print("\n")
    end
  end
end

class Robot
  def initialize(start_x, start_y, step_x, step_y)
    @location = Point.new(start_x.to_i, start_y.to_i)
    @step_x = step_x.to_i
    @step_y = step_y.to_i
  end

  def current_location
    @location
  end

  def quadrant
    @location.quadrant
  end

  def to_s
    "Robot at #{@location}"
  end

  def step
    @location = @location.moved_by(@step_x, @step_y)
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