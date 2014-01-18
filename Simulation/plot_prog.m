
%% Initialization
clear ; close all; clc

%% ========== Customizable Zone ===========

plot_mode = 2;


input_file = 'generated_files/run_output.csv';
track_file = 'generated_files/track.csv';
car_file =   'generated_files/car_data.csv';
sense_file = 'generated_files/sense_output.csv';


%% ========== End Customizable Zone ===========
%% ========== Do NOT Modify Anything Below This Line ===========

%% =========== Part 1: Loading The Data =============

% Load Training Data
fprintf('Loading Data ...\n')

D = dlmread(input_file);
T = dlmread(track_file);
C = dlmread(car_file);
S = dlmread(sense_file);

car_length = C(1);
sensor_offset = C(2);
sensor_width = C(3);
wheel_length = 0.1;
wheel_width = 0.05;


%% =========== Part 2: Plotting The Data =============

plot(T(:,1), T(:,2), 'k', 'LineWidth', 2)
hold on;

if plot_mode == 1,
	plot(D(:,1), D(:,2), 'r', 'LineWidth', 3)
	plot(S(:,1), S(:,2), 'g', 'LineWidth', 3)
end

if plot_mode == 2,
	plot(D(:,1), D(:,2), 'r', 'LineWidth', 3)
	plot(S(:,1), S(:,2), 'g', 'LineWidth', 3)
	%plot(S(:,3), S(:,4), 'bo', 'LineWidth', 3)
	
	figure
	hold on;
	plot(D(:,5), 'r', 'LineWidth', 3)
	plot(D(:,6), 'b', 'LineWidth', 3)

end

if plot_mode == 3,
	
	for k=1:15:length(D)
		x1 = D(k,1);
		y1 = D(k,2);
		theta = D(k,3);
		x2 = x1+cos(theta)*car_length;
		y2 = y1+sin(theta)*car_length;
		plot([x1; x2], [y1; y2], 'b','LineWidth',5)
		%Connector 
		x3 = x1+cos(theta)*sensor_offset;
		y3 = y1+sin(theta)*sensor_offset;
		plot([x2; x3], [y2; y3], 'b','LineWidth',1)
		%Sensor
		x4 = x3-sin(theta)*sensor_width;
		y4 = y3+cos(theta)*sensor_width;
		x5 = x3+sin(theta)*sensor_width;
		y5 = y3-cos(theta)*sensor_width;
		plot([x4; x5], [y4; y5], 'b','LineWidth',2)
		
		%Steering Command
		steercmd_theta = D(k,5);
			%right wheel
			x6 = x2+sin(theta)*wheel_width;
			y6 = y2-cos(theta)*wheel_width;
			x7 = x6+car_length*wheel_length*cos(theta+steercmd_theta);
			y7 = y6+car_length*wheel_length*sin(theta+steercmd_theta);
			x8 = x6-car_length*wheel_length*cos(theta+steercmd_theta);
			y8 = y6-car_length*wheel_length*sin(theta+steercmd_theta);
			plot([x7; x8], [y7; y8], 'r','LineWidth',1)
			
			%left wheel
			x9 = x2-sin(theta)*wheel_width;
			y9 = y2+cos(theta)*wheel_width;    
			x10 = x9+car_length*wheel_length*cos(theta+steercmd_theta);
			y10 = y9+car_length*wheel_length*sin(theta+steercmd_theta);
			x11 = x9-car_length*wheel_length*cos(theta+steercmd_theta);
			y11 = y9-car_length*wheel_length*sin(theta+steercmd_theta);
			plot([x10; x11], [y10; y11], 'r','LineWidth',1)
			
		%Back wheels
			%right wheel
			x12 = x1+sin(theta)*wheel_width;
			y12 = y1-cos(theta)*wheel_width;
			x13 = x12+car_length*wheel_length*cos(theta);
			y13 = y12+car_length*wheel_length*sin(theta);
			x14 = x12-car_length*wheel_length*cos(theta);
			y14 = y12-car_length*wheel_length*sin(theta);
			plot([x13; x14], [y13; y14], 'r','LineWidth',1)
			
			%left wheel
			x15 = x1-sin(theta)*wheel_width;
			y15 = y1+cos(theta)*wheel_width;    
			x16 = x15+car_length*wheel_length*cos(theta);
			y16 = y15+car_length*wheel_length*sin(theta);
			x17 = x15-car_length*wheel_length*cos(theta);
			y17 = y15-car_length*wheel_length*sin(theta);
			plot([x16; x17], [y16; y17], 'r','LineWidth',1)
	end
    
end

pause
