% UNIVERSIDAD DEL VALLE DE GUATEMALA
% Inteligencia Artificial - CC3085
%
% Elda Daniela Navas Cinto - 211000
% Proyecto Final - Construcción de Dataset

% Limpiar espacio
close all; clear; clc;

% Definir parámetros
Fs = 2000;                % Frecuencia de muestreo (Hz)
tamano_ventana = 5;       % s 
N = Fs * tamano_ventana;  % Número de Muetras
f = Fs*(0:(N/2))/N;       % Vector de frecuencias

% Filtrado Señal
f_low = 20;  % Frecuencia de corte inferior (20 Hz)
f_high = 500;  % Frecuencia de corte superior (500 Hz)
Wn = [f_low f_high] / (Fs / 2);  % Frecuencias normalizadas
[b, a] = butter(4, Wn, 'bandpass');  % Diseñar el filtro Butterworth pasabanda Orden 4

% Cargar datos (variable 'data')
reposo = load('Reposo.mat', 'data');
palma = load('Palma.mat', 'data');
pinza = load('Pinza.mat', 'data');
puno = load('Puño.mat', 'data');

% Extraer y filtrar la variable 'data' de cada estructura
reposo = filter(b, a, reposo.data);
palma = filter(b, a, palma.data);
pinza = filter(b, a, pinza.data);
puno = filter(b, a, puno.data);

%% DATASET REPOSO
% Inicializar dataset para Reposo
dataset_reposo = [];

num_ventanas_rep = floor(length(reposo) / N); % Número de ventanas 

% Recorrer cada 2 ventanas para extraer características
for i = 1:num_ventanas_rep
    ventana = reposo((i-1)*N+1:i*N); % Extraer la ventana de 5 segundos
    
    % Extraer características en dominio de tiempo
    MAV = mean(abs(ventana));      % Mean Absolute Value
    RMS = sqrt(mean(ventana.^2));  % Root Mean Square
    V = var(ventana);              % Varianza
    WL = sum(abs(diff(ventana)));  % Waveform Length
    SSC = sum(diff(ventana) > 0);  % Slope Sign Changes
    IEMG = sum(abs(ventana));      % Integral of EMG
    LOGVAR = log(var(ventana));  % Log-variance
    
    % Transformada de Fourier FFT
    Y = fft(ventana);           % Transformada de Fourier
    Y = abs(Y/N);               % Magnitud normalizada
    Y = Y(1:N/2+1);             % Solo el espectro positivo
    Y(2:end-1) = 2*Y(2:end-1);  % Escala adecuada

    % Extraer características en dominio de frecuencia usando FFT
    PF = f(find(Y == max(Y), 1));  % Peak Frequency
    TP = sum(Y.^2);                % Total Power
    SE = -sum((Y ./ sum(Y)) .* log(Y ./ sum(Y)));                                         % Spectral Entropy
    FR = sum(Y(f >= 50 & f <= 150)) / sum(Y(f >= 0 & f <= 500));                          % Frequency Ratio (50-150 Hz)
    BW = f(find(Y >= 0.5 * max(Y), 1, 'first')) - f(find(Y >= 0.5 * max(Y), 1, 'last'));  % Bandwidth
    P2P = max(Y) - min(Y);         % Peak-to-Peak
    PSD = sum(Y.^2);               % Power Spectral Density (potencia total)
    MOV = "reposo";

    % Guardar caracterísitcas en el dataset
    dataset_reposo = [dataset_reposo; MAV, RMS, V, WL, SSC, IEMG, LOGVAR, PF, TP, SE, FR, BW, PSD, P2P, MOV];
end

% Guardar el dataset en un archivo .mat
save('dataset_reposo.mat', 'dataset_reposo');

%% DATASET PALMA EXTENDIDA
% Inicializar dataset para Palma
dataset_palma = [];

num_ventanas = floor(length(palma) / N); % Número de ventanas 

% Recorrer cada 2 ventanas para extraer características
for i = 1:2:num_ventanas
    ventana = palma((i-1)*N+1:i*N); % Extraer la ventana de 5 segundos
    
    % Extraer características en dominio de tiempo
    MAV = mean(abs(ventana));      % Mean Absolute Value
    RMS = sqrt(mean(ventana.^2));  % Root Mean Square
    V = var(ventana);              % Varianza
    WL = sum(abs(diff(ventana)));  % Waveform Length
    SSC = sum(diff(ventana) > 0);  % Slope Sign Changes
    IEMG = sum(abs(ventana));      % Integral of EMG
    LOGVAR = log(var(ventana));  % Log-variance
    
    % Transformada de Fourier FFT
    Y = fft(ventana);           % Transformada de Fourier
    Y = abs(Y/N);               % Magnitud normalizada
    Y = Y(1:N/2+1);             % Solo el espectro positivo
    Y(2:end-1) = 2*Y(2:end-1);  % Escala adecuada

    % Extraer características en dominio de frecuencia usando FFT
    PF = f(find(Y == max(Y), 1));  % Peak Frequency
    TP = sum(Y.^2);                % Total Power
    SE = -sum((Y ./ sum(Y)) .* log(Y ./ sum(Y)));                                         % Spectral Entropy
    FR = sum(Y(f >= 50 & f <= 150)) / sum(Y(f >= 0 & f <= 500));                          % Frequency Ratio (50-150 Hz)
    BW = f(find(Y >= 0.5 * max(Y), 1, 'first')) - f(find(Y >= 0.5 * max(Y), 1, 'last'));  % Bandwidth
    P2P = max(Y) - min(Y);         % Peak-to-Peak
    PSD = sum(Y.^2);               % Power Spectral Density (potencia total)
    MOV = "palma";

    % Guardar caracterísitcas en el dataset
    dataset_palma = [dataset_palma; MAV, RMS, V, WL, SSC, IEMG, LOGVAR, PF, TP, SE, FR, BW, PSD, P2P, MOV];
end

% Guardar el dataset en un archivo .mat
save('dataset_palma.mat', 'dataset_palma');

%% DATASET PINZA
% Inicializar dataset para Pinza
dataset_pinza = [];

% Recorrer cada 2 ventanas para extraer características
for i = 1:2:num_ventanas
    ventana = pinza((i-1)*N+1:i*N); % Extraer la ventana de 5 segundos
    
    % Extraer características en dominio de tiempo
    MAV = mean(abs(ventana));      % Mean Absolute Value
    RMS = sqrt(mean(ventana.^2));  % Root Mean Square
    V = var(ventana);              % Varianza
    WL = sum(abs(diff(ventana)));  % Waveform Length
    SSC = sum(diff(ventana) > 0);  % Slope Sign Changes
    IEMG = sum(abs(ventana));      % Integral of EMG
    LOGVAR = log(var(ventana));  % Log-variance
    
    % Transformada de Fourier FFT
    Y = fft(ventana);           % Transformada de Fourier
    Y = abs(Y/N);               % Magnitud normalizada
    Y = Y(1:N/2+1);             % Solo el espectro positivo
    Y(2:end-1) = 2*Y(2:end-1);  % Escala adecuada

    % Extraer características en dominio de frecuencia usando FFT
    PF = f(find(Y == max(Y), 1));  % Peak Frequency
    TP = sum(Y.^2);                % Total Power
    SE = -sum((Y ./ sum(Y)) .* log(Y ./ sum(Y)));                                         % Spectral Entropy
    FR = sum(Y(f >= 50 & f <= 150)) / sum(Y(f >= 0 & f <= 500));                          % Frequency Ratio (50-150 Hz)
    BW = f(find(Y >= 0.5 * max(Y), 1, 'first')) - f(find(Y >= 0.5 * max(Y), 1, 'last'));  % Bandwidth
    P2P = max(Y) - min(Y);         % Peak-to-Peak
    PSD = sum(Y.^2);               % Power Spectral Density (potencia total)
    MOV = "pinza";

    % Guardar caracterísitcas en el dataset
    dataset_pinza = [dataset_pinza; MAV, RMS, V, WL, SSC, IEMG, LOGVAR, PF, TP, SE, FR, BW, PSD, P2P, MOV];
end

% Guardar el dataset en un archivo .mat
save('dataset_pinza.mat', 'dataset_pinza');

%% DATA SET PUÑO CERRADO
% Inicializar dataset para Puño
dataset_puno = [];

% Recorrer cada 2 ventanas para extraer características
for i = 1:2:num_ventanas
    ventana = puno((i-1)*N+1:i*N); % Extraer la ventana de 5 segundos
    
    % Extraer características en dominio de tiempo
    MAV = mean(abs(ventana));      % Mean Absolute Value
    RMS = sqrt(mean(ventana.^2));  % Root Mean Square
    V = var(ventana);              % Varianza
    WL = sum(abs(diff(ventana)));  % Waveform Length
    SSC = sum(diff(ventana) > 0);  % Slope Sign Changes
    IEMG = sum(abs(ventana));      % Integral of EMG
    LOGVAR = log(var(ventana));  % Log-variance
    
    % Transformada de Fourier FFT
    Y = fft(ventana);           % Transformada de Fourier
    Y = abs(Y/N);               % Magnitud normalizada
    Y = Y(1:N/2+1);             % Solo el espectro positivo
    Y(2:end-1) = 2*Y(2:end-1);  % Escala adecuada

    % Extraer características en dominio de frecuencia usando FFT
    PF = f(find(Y == max(Y), 1));  % Peak Frequency
    TP = sum(Y.^2);                % Total Power
    SE = -sum((Y ./ sum(Y)) .* log(Y ./ sum(Y)));                                         % Spectral Entropy
    FR = sum(Y(f >= 50 & f <= 150)) / sum(Y(f >= 0 & f <= 500));                          % Frequency Ratio (50-150 Hz)
    BW = f(find(Y >= 0.5 * max(Y), 1, 'first')) - f(find(Y >= 0.5 * max(Y), 1, 'last'));  % Bandwidth
    P2P = max(Y) - min(Y);         % Peak-to-Peak
    PSD = sum(Y.^2);               % Power Spectral Density (potencia total)
    MOV = "puno";

    % Guardar caracterísitcas en el dataset
    dataset_puno = [dataset_puno; MAV, RMS, V, WL, SSC, IEMG, LOGVAR, PF, TP, SE, FR, BW, PSD, P2P, MOV];
end

% Guardar el dataset en un archivo .mat
save('dataset_puno.mat', 'dataset_puno');

%% CONCATENAR TODAS LAS BASES
close all; clear; clc;

% Cargar los datasets
load('dataset_reposo.mat'); % Cargar dataset_reposo
load('dataset_palma.mat');  % Cargar dataset_palma
load('dataset_pinza.mat');  % Cargar dataset_pinza
load('dataset_puno.mat');   % Cargar dataset_puno

% Concatenar los datos en un solo dataset
dataset_completo = [dataset_reposo; dataset_palma; dataset_pinza; dataset_puno]; 

% Crear el encabezado
encabezado = {'MAV', 'RMS', 'V', 'WL', 'SSC', 'IEMG', 'LOGVAR', 'PF', 'TP', 'SE', 'FR', 'BW', 'PSD', 'P2P', 'MOV'};

% Escribir el dataset combinado en un archivo CSV
csvwrite_with_headers('dataset_completo.csv', dataset_completo, encabezado);

% Función para escribir CSV con encabezado
function csvwrite_with_headers(filename, data, headers)
    % Abrir el archivo para escribir
    fid = fopen(filename, 'w');
    
    % Escribir los encabezados
    fprintf(fid, '%s,', headers{1:end-1});
    fprintf(fid, '%s\n', headers{end});
    
    % Escribir los datos
    for i = 1:size(data, 1)
        fprintf(fid, '%f,', data(i, 1:end-1));
        fprintf(fid, '%s\n', data{i, end});
    end
    
    % Cerrar el archivo
    fclose(fid);
end
