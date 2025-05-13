% UNIVERSIDAD DEL VALLE DE GUATEMALA
% Inteligencia Artificial - CC3085
%
% Elda Daniela Navas Cinto - 211000
% Proyecto Final - Elaboración de Gráficas

% Limpiar espacio
close all; clear; clc;

% Definir parámetros
Fs = 2000;                % Frecuencia de muestreo (Hz)
tamano_ventana = 5;       % s 
N = Fs * tamano_ventana;  % Número de Muetras

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

% Extraer la variable 'data' de cada estructura
reposo = reposo.data;
palma = palma.data;
pinza = pinza.data;
puno = puno.data;

% Definir inicio y fin del primer movimiento
inicio_movimiento = ( Fs * tamano_ventana * 3) + 1;                  
fin_movimiento = inicio_movimiento + N - 1; 

% Cortar y filtrar segmentos de interés
reposo_segmento = filter(b, a, reposo(inicio_movimiento:fin_movimiento));
palma_segmento = filter(b, a, palma(inicio_movimiento:fin_movimiento));
pinza_segmento = filter(b, a, pinza(inicio_movimiento:fin_movimiento));
puno_segmento = filter(b, a, puno(inicio_movimiento:fin_movimiento));

% Crear vector de tiempo de 0 a 5 segundos
t = linspace(0,5,N);

% Graficar Señal
figure(1);

subplot(2,2,1);
plot(t, reposo_segmento, 'Color', [0 0.4470 0.7410]); 
title('Reposo', 'FontSize', 14);
xlabel('Tiempo (s)');
ylabel('Amplitud (mV)');
ylim([-1 1]);

subplot(2,2,2);
plot(t, palma_segmento, 'Color', [0.8500 0.3250 0.0980]); 
title('Palma Extendida', 'FontSize', 14);
xlabel('Tiempo (s)');
ylabel('Amplitud (mV)');
ylim([-1 1]);

subplot(2,2,3);
plot(t, pinza_segmento, 'Color', [0.4660 0.6740 0.1880]); 
title('Pinza', 'FontSize', 14);
xlabel('Tiempo (s)');
ylabel('Amplitud (mV)');
ylim([-1 1]);

subplot(2,2,4);
plot(t, puno_segmento, 'Color', [0.4940 0.1840 0.5560]); 
title('Puño Cerrado', 'FontSize', 14);
xlabel('Tiempo (s)');
ylabel('Amplitud (mV)');
ylim([-1 1]);

sgtitle('Patrones Musculares', 'FontSize', 28, 'FontWeight', 'bold');

%% TRANSFORMADA DE FOURIER
f = Fs*(0:(N/2))/N; % Vector de frecuencias

% FFT
Y_reposo = fft(reposo_segmento);
Y_reposo = abs(Y_reposo/N);
Y_reposo = Y_reposo(1:N/2+1);
Y_reposo(2:end-1) = 2*Y_reposo(2:end-1);

Y_palma = fft(palma_segmento);
Y_palma = abs(Y_palma/N);
Y_palma = Y_palma(1:N/2+1);
Y_palma(2:end-1) = 2*Y_palma(2:end-1);

Y_pinza = fft(pinza_segmento);
Y_pinza = abs(Y_pinza/N);
Y_pinza = Y_pinza(1:N/2+1);
Y_pinza(2:end-1) = 2*Y_pinza(2:end-1);

Y_puno = fft(puno_segmento);
Y_puno = abs(Y_puno/N);
Y_puno = Y_puno(1:N/2+1);
Y_puno(2:end-1) = 2*Y_puno(2:end-1);

% Gráficas con stem
figure(2);

subplot(2,2,1);
stem(f, Y_reposo, 'Color', [0 0.4470 0.7410]);
title('Reposo', 'FontSize', 14);
xlabel('Frecuencia (Hz)');
ylabel('|P(f)|');
xlim([0 1000]);
ylim([0 0.016]);

subplot(2,2,2);
stem(f, Y_palma, 'Color', [0.8500 0.3250 0.0980]);
title('Palma Extendida', 'FontSize', 14);
xlabel('Frecuencia (Hz)');
ylabel('|P(f)|');
xlim([0 1000]);
ylim([0 0.016]);

subplot(2,2,3);
stem(f, Y_pinza, 'Color', [0.4660 0.6740 0.1880]);
title('Pinza', 'FontSize', 14);
xlabel('Frecuencia (Hz)');
ylabel('|P(f)|');
xlim([0 1000]);
ylim([0 0.016]);

subplot(2,2,4);
stem(f, Y_puno, 'Color', [0.4940 0.1840 0.5560]);
title('Puño Cerrado', 'FontSize', 14);
xlabel('Frecuencia (Hz)');
ylabel('|P(f)|');
xlim([0 1000]);
ylim([0 0.016]);

sgtitle('Espectro Unilateral de la Señal', 'FontSize', 28, 'FontWeight', 'bold');


