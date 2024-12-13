using JuMP , GLPK, CSV

function main()
	minimum_tokens = 0
	for row in CSV.File("input.csv")
		effect_a_x = row.effect_a_x
		effect_a_y = row.effect_a_y
		effect_b_x = row.effect_b_x
		effect_b_y = row.effect_b_y
		prize_x = row.prize_x
		prize_y = row.prize_y

		d1 = Model(GLPK.Optimizer)
		@variable(d1 , a_presses >= 0, Int)
		@variable(d1 , b_presses >= 0, Int)

		@constraint(d1, a_presses * effect_a_x + b_presses * effect_b_x == prize_x)
		@constraint(d1, a_presses * effect_a_y + b_presses * effect_b_y == prize_y)
		@constraint(d1, a_presses <= 100)
		@constraint(d1, b_presses <= 100)
		@objective(d1, Min, 3*a_presses + b_presses)

		optimize!(d1)
		if(result_count(d1) > 0)
			minimum_tokens += objective_value(d1)
		end
	end
	println(minimum_tokens)
end

main()