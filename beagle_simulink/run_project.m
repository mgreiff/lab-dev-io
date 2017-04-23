%% Top level settings
% Here, the model which is to be simulated is set (h) with a controller (c)
% which is then simulated in a specified time (t). To change model or 
% controller parameters, alter the corresponding init file or the
% appropriate parameter in the workspace. No parameters are hard coded in
% the simulink models themselves. The default setting simulates a DC motor
% with a conditional anti-windup scheme in continuous time.
%
% Valid options are:
%
% model:
%     'DC_motor'        - An LTI motor model with load torque.
%     'furuta_pendulum' - A non-linear pendulum model.
%     'ball_and_beam'   - A non-linear ball and beam model.
% c:
%     'feedback'   - Linear feedback law with pp -1+-i (c) or 0 (d)
%     'PID'        - Regular PID controller
%     'PIDAW'      - PID controller with conditional anti-windup (AW)
%     'PIDcascade' - Cascade control loop for position control with AW
%     'LQRi'       - LQR with inegrator states for elimination of ss error
%     'LQRp'       - Precompensated LQR for good trajectory following
%     'MRAC'       - Adaptive control with reference model poles in -1+-i
%     'SMC'        - Sliding mode control with respect to angular position
% t:
%     'continuous'  - Simulates model and controller in continuous time
%     'discrete'    - Simulates model and discrete in continuous time
%
% Functional combinations are
% 
%                    DC_motor   Furuta   BeamBall(1D)   BeamBall(2D)  Cubes
%     'response'       1/1       1/0         0/0            0/0        0/0
%     'feedback'       0/0       0/0         0/0            0/0        0/0
%     'PID'            1/1       0/0         0/0            0/0        0/0
%     'PIDAW'          1/1       0/0         0/0            0/0        0/0
%     'PIDcascade'     0/1       0/0         0/0            0/0        0/0
%     'LQRi'           1/0       0/0         0/0            0/0        0/0
%     'LQRp'           1/0       0/0         0/0            0/0        0/0
%     'MRAC'           1/1       0/0         0/0            0/0        0/0
%     'SMC'            1/0       0/0         0/0            0/0        0/0

close all;
clear;

% Settings
model =  'furuta_pendulum';
controller = 'response';
time = 'continuous';


%% Check that the input data is valid
status = 1;
models = {'DC_motor', 'furuta_pendulum', 'ball_and_beam', 'balancing_cube'};
controllers = {'response', 'PID', 'PIDAW', 'PIDcascade', 'LQRp', 'LQRi', 'MRAC', 'SMC'};
times = {'continuous', 'discrete'};

matches = strfind(models,model);
if ~any(vertcat(matches{:})) 
    fprintf(['The hardware model "', model,'" does not exist in the library.'])
    fprintf('Valid choices are:\n\n')
    disp(cellstr(models'))
    status = 0;
end

matches = strfind(controllers,controller);
if ~any(vertcat(matches{:})) 
    fprintf(['The controller ', controller, ' does not exist in the library.'])
    fprintf('Valid choices are:\n\n')
    disp(cellstr(controllers'))
    status = 0;
end

matches = strfind(times,time);
if ~any(vertcat(matches{:})) 
    fprintf(['The specified time ', time, ' does not exist in the library.'])
    fprintf('Valid choices are: continuous and discrete.')
    status = 0;
end

%% Add all simulink folders to path
if status == 1
    try
        addpath([pwd, '/controllers/general']);
        addpath([pwd, '/models']);
        for ii = 1:length(models)
            addpath([pwd, '/initialization/', models{ii}]);
            addpath([pwd, '/controllers/', models{ii}]);
        end
    catch
        fprintf(['Filesystem incompatibilities, check that there exists a ',...
                 'direcotry for ', model, ' in /controller and /initialization'])
        status = 0;
    end
end

%% Run init files
if status == 1
    fprintf('Initializing... ')
    try
        run(['init_', model, '.m'])
        if ~strcmp('response', controller)
            run(['init_', model, '_', controller, '_', time(1), '.m'])
        end
        fprintf('Done!')
    catch
        fprintf(['Failed!\nThe initialization file "init_', model, '_',...
                  controller, '_', time(1), '.m" could not be found.\n'])
        status = 0;
    end
end

%% Open and simulate model
if status == 1
    try
        fprintf(['\nSimulating a ', model, ' with ', controller, ' in ',...
                 time, ' time... '])

        if strcmp('response', controller)
            open([model, '_', controller]);
            sim([model, '_', controller]);
        else
            run(['init_', model, '_', controller, '_', time(1), '.m'])
            open([model, '_', controller, '_', time(1)]);
            sim([model, '_', controller, '_', time(1)]);
        end
        fprintf('Done!\n')
    catch
        fprintf(['Failed!\nThe controller may not be supported in ',...
                 time, ' time just yet.\n'])
        status = 0;
    end
end
    