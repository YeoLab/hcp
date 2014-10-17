import pytest
import numpy as np
from hcp import hcp



class TestClass:

		
		# Helper method to retrieve correct results from Matlab tests
		def parse_matlab_data(self, test_name, iterations):
			
			# Read in Output from Matlab Tests
			matlab_results = open('matlab_test_results.txt', 'r')
			results_lines = matlab_results.readlines()
			
			var0 = np.array([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]])
			var1 = np.array([[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]])
			var2 = np.array([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]])
			var3 = np.zeros(iterations)
			
			read_data = 0
			current_var = -1
			var0_row_counter = 0
			var1_row_counter = 0
			var2_row_counter = 0
			var3_index = 0
			num = ''
			for line in results_lines:
				if test_name in line:
					read_data = 1
				
				if read_data == 1:
					
					if current_var == 0 and var0_row_counter < 3:
						line = line.replace("\n", "")   # Remove newline character
						row = line.split(',')
						
						var0[var0_row_counter,0] = row[0]
						var0[var0_row_counter,1] = row[1]
						var0_row_counter += 1
						
					if current_var == 1 and var1_row_counter < 2:
						line = line.replace("\n", "")   # Remove newline character
						row = line.split(',')
										
						var1[var1_row_counter,0] = row[0]
						var1[var1_row_counter,1] = row[1]
						var1[var1_row_counter,2] = row[2]
						var1[var1_row_counter,3] = row[3]					
						var1_row_counter += 1			
						
					if current_var == 2 and var2_row_counter < 4:
						line = line.replace("\n", "")   # Remove newline character
						row = line.split(',')
			
						var2[var2_row_counter,0] = row[0]
						var2[var2_row_counter,1] = row[1]
						var2_row_counter += 1
												
					if current_var == 3 and var3_index < iterations:
			
						
			
						for char in line:
							if char == '.' or char.isdigit():
								num = num + char
							elif char == ',':
								var3[var3_index] = float(num)
								var3_index += 1
								num = ''
								
						if var3_index == iterations-1:
							var3[var3_index] = float(num)
							var3_index += 1
			
			
										
					# Determine what var data to read
					if '@' in line:
						current_var = 0
					if '#' in line:
						current_var = 1
					if '$' in line:
						current_var = 2
					if '%' in line:
						current_var = 3
					if '^' in line:
						current_var = -1	
						read_data = 0	
						
						
			return var0, var1, var2, var3
			
			
			
		def test_1(self):
			# Execute Python Code on Test Data
			F = np.array([[1,1,1,1],[2,2,2,2],[3,3,3,3]])
			Y = np.array([[4,4,4,4],[5,5,5,5],[6,6,6,6]])
			
			k = 2	
			lam1 = 1
			lam2 = 2
			lam3 = 1
			
			iterations = 100
			var = hcp(F,Y,k,lam1, lam2, lam3, iterations)
		
			matlab_var = self.parse_matlab_data('test_1', iterations)
		
			
			matlab_converging_value = matlab_var[3]
			python_array = var[3]
			python_converging_value_array_form = python_array[99]
			python_converging_value = python_converging_value_array_form[0]
			python_converging_value = python_converging_value.round(3)

			# Assert that the converging #'s are the same						
			assert python_converging_value == matlab_converging_value[99]	
		