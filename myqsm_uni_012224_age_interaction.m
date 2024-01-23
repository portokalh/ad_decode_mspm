% List of open inputs
nrun = X; % enter the number of runs here
jobfile = {'/Users/alex/Documents/MATLAB/ad_decode/myqsm_uni_012224_age_interaction_job.m'};
jobs = repmat(jobfile, 1, nrun);
inputs = cell(0, nrun);
for crun = 1:nrun
end
spm('defaults', 'PET');
spm_jobman('run', jobs, inputs{:});
