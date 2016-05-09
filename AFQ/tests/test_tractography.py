import os.path as op
import numpy.testing as npt

import nibabel.tmpdirs as nbtmp

from AFQ.csd import fit_csd
from AFQ.dti import fit_dti
from AFQ.tractography import track
from AFQ.utils.testing import make_tracking_data


def test_csd_deterministic():
    with nbtmp.InTemporaryDirectory() as tmpdir:
        fbval = op.join(tmpdir, 'dti.bval')
        fbvec = op.join(tmpdir, 'dti.bvec')
        fdata = op.join(tmpdir, 'dti.nii.gz')
        make_tracking_data(fbval, fbvec, fdata)
        for sh_order in [4, 8, 10]:
            fname = fit_csd(fdata, fbval, fbvec,
                            response=((0.0015, 0.0003, 0.0003), 100),
                            sh_order=8, lambda_=1, tau=0.1, mask=None,
                            out_dir=tmpdir)
            for directions in ["det", "prob"]:
                sl = track(fname, directions,
                           max_angle=30., sphere=None,
                           seed_mask=None,
                           seed_density=[1, 1, 1],
                           stop_mask=None,
                           stop_threshold=0.2,
                           step_size=0.5)

        # Generate the first streamline:
        sl0 = next(sl._generate_streamlines())
        npt.assert_equal(sl0.shape[-1], 3)


def test_dti_deterministic():
    with nbtmp.InTemporaryDirectory() as tmpdir:
        fbval = op.join(tmpdir, 'dti.bval')
        fbvec = op.join(tmpdir, 'dti.bvec')
        fdata = op.join(tmpdir, 'dti.nii.gz')
        make_tracking_data(fbval, fbvec, fdata)
        fdict = fit_dti(fdata, fbval, fbvec)
        for directions in ["det", "prob"]:
            sl = track(fdict['params'],
                       directions,
                       max_angle=30.,
                       sphere=None,
                       seed_mask=None,
                       seed_density=[1, 1, 1],
                       stop_mask=None,
                       stop_threshold=0.2,
                       step_size=0.5)

        # Generate the first streamline:
        sl0 = next(sl._generate_streamlines())
        npt.assert_equal(sl0.shape[-1], 3)