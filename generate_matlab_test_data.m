function generate_matlab_test_data()


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%% TEST 1 %%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  F = [1,1,1,1;2,2,2,2;3,3,3,3];
  Y = [4,4,4,4;5,5,5,5;6,6,6,6];

  k = 2;
  lam1 = 1;
  lam2 = 2;
  lam3 = 1;

  [var1, var2, var3, var4] = hidden_covariate_linear(F,Y,k,lam1, lam2, lam3,100);

  fullpath = which(mfilename);
  c = strfind(fullpath, 'generate_matlab_test_data');
  desired_path = fullpath(1:c-1);
  file_to_open = strcat(desired_path, 'matlab_test_results.txt');

  file = fopen(file_to_open,'w');

  % Declare name of pytest function to associate this data with.
  fprintf(file, 'test_1 \n') ;

  symbol1 = '@'; % indicator symbol for var1
  dlmwrite(file_to_open, symbol1, '-append');
  dlmwrite(file_to_open, var1, '-append');

  symbol2 = '#'; % indicator symbol for var2
  dlmwrite(file_to_open, symbol2, '-append');
  dlmwrite(file_to_open, var2, '-append');

  symbol3 = '$'; % indicator symbol for var3
  dlmwrite(file_to_open, symbol3, '-append');
  dlmwrite(file_to_open, var3, '-append');

  symbol4 = '%'; % indicator symbol for var4
  dlmwrite(file_to_open, symbol4, '-append');
  dlmwrite(file_to_open, var4, '-append');

  symbol5 = '^'; % indicator that test data has ended
  dlmwrite(file_to_open, symbol5, '-append');



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%% END TEST 1 %%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


  fclose(file);
  fprintf('Tests Done. \nFile "matlab_test_results.txt" generated. \n') 
