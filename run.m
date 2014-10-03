%load sailfish_expression_covariates.mat

april_data = importdata('~/scratch/dropbox/Dropbox (ACE Lab)/ASD_Signature/sailfish/all_plates/expression.tsv')
Y = april_data.data';
samples = april_data.textdata(1,2:end);
genes = april_data.textdata(2:end,1);
clear april_data

april_labels = importdata('~/scratch/dropbox/Dropbox (ACE Lab)/ASD_Signature/sailfish/all_plates/classes.tsv','\t',1)
labels = april_labels.data; 
labels(labels == 2) = 0; % Autistic=1, Control=0
patients1 = april_labels.textdata(2:end,1);
clear april_labels

april_metadata = importdata('~/scratch/dropbox/Dropbox (ACE Lab)/ASD_Signature/sailfish/all_plates/metadata_6f.tsv','\t',1)
metadata = april_metadata.data(:,[end 1:end-1]);
F = metadata;
patients2 = april_metadata.textdata(2:end,1);

clear april_metadata

samples_match_patients1 = all(cellfun(@strcmp, samples', patients1))
samples_match_patients2 = all(cellfun(@strcmp, samples', patients2))
labels_match_metadata = all((labels==1) == (metadata(:,1)==1))

save july_expression_metadata.mat
%load july_expression_metadata.mat

%%



% input data: Y (matrix of gene expression, nxg where n is number of subjects and g is number of genes);
%             F (matrix of known covariates, nxd where d is number of covariates)


% (2) standardize the data

Yn = standardize(Y')';
Yn(isnan(Yn)) = 0;
size(Yn)

Fn = standardize(F(:,[1:2 4:end])')';
Fn(isnan(Fn)) = 0;
size(Fn)
% (4) set the model parameters

k = 10;
lambda = 1;
lambda2 = 1;
lambda3 = 1;
iter = 1000;

% (5) run HCP

[X,W,B,o] = hidden_covariates_model(Fn,Yn,k,lambda,lambda2,lambda3,iter);

% (6) get the residual data:

Res = Yn-X*W;

save july_expression_covariates_s651_h10_i1000.mat
return % done with headless TSCC

%% Visualize
load july_expression_covariates_s651_h10_i1000.mat
%[temp, samplesByPlate] = sort(F(:,3));
samplesByPlate = 1:size(F,1);
[temp, hiddenByPlateEffect] = sort(sum(abs(B),1))

addpath ~/code/cbrewer/
addpath cm_and_cb_utilities/

scrsz = get(0,'ScreenSize');
figure('Position',[1 scrsz(4) scrsz(3) scrsz(4)],'PaperPositionMode','auto');

GS = 5;
GSM = reshape(1:GS*GS, [GS GS])';

%subplot(GS,GS,GSM(1:end-1,1))
figure('Position',[1 scrsz(4) scrsz(3)/4 3*scrsz(4)/4],'PaperPositionMode','auto');
h = imagesc(X(samplesByPlate,hiddenByPlateEffect)); 
ylabel('train samples')
set(gca,'xTick',[])
title('X','FontSize',30,'FontName','Lucida Handwriting')
colormap(b2r(min(X(:)),max(X(:))))
colorbar
cbfreeze

%subplot(GS,GS,GSM(end,1))
figure('Position',[1 3*scrsz(4)/4 scrsz(3)/4 scrsz(4)/4],'PaperPositionMode','auto');
imagesc(B(:,hiddenByPlateEffect));
set(gca,'yTick',1:size(F,2),'yTickLabel',{'ASD','age','PID_XX','rand'}) % {'age','rand','plate','sex','ASD'})
xlabel('hidden covariates')
title('B','FontSize',30,'FontName','Lucida Handwriting')
colormap(b2r(min(B(:)),max(B(:))))
colorbar
cbfreeze

%subplot(GS,GS,vec(GSM(1:end-1,2:end)))
figure('Position',[scrsz(3)/4 scrsz(4) 3*scrsz(3)/4 3*scrsz(4)/4],'PaperPositionMode','auto');
imagesc(Res(samplesByPlate,:));
title('Y - XW','FontSize',30,'FontName','Lucida Handwriting')
set(gca,'xTick',[])
colormap(b2r(min(Res(:)),max(Res(:))))
colorbar
cbfreeze

%subplot(GS,GS,GSM(end,2:end))
figure('Position',[1 3*scrsz(4)/4 3*scrsz(3)/4 scrsz(4)/4],'PaperPositionMode','auto');
imagesc(W);
xlabel('genes')
title('W','FontSize',30,'FontName','Lucida Handwriting')
colormap(b2r(min(W(:)),max(W(:))))
colorbar
cbfreeze

%%

%% clustering
% cg = clustergram(Z, ...
%             %'RowLabels', JR.cells, 'ColumnLabels', JR.genes, ...
%             'Standardize','column','Cluster','row', 'OptimalLeafOrder', true, ...
%             'ColumnPDist', 'Euclidean', 'RowPDist', 'Euclidean', 'Linkage', 'average')
