#pragma once

/// A collection of multi-variate regression polynomials for engine parameters
class Polynomial {
public:
	double n2NX(double n2, double preN2, double idleN2) {
		double n2_out = 0;
		double norm_n2 = 0;

		norm_n2 = n2 * 68.2 / idleN2;

		double n2_coef[16] = {
			4.03649879e+00, -9.41981960e-01, 1.98426614e-01, -2.11907840e-02,
			1.00777507e-03, -1.57319166e-06, -2.15034888e-06, 1.08288379e-07,
			-2.48504632e-09, 2.52307089e-11, -2.06869243e-14, 8.99045761e-16,
			-9.94853959e-17, 1.85366499e-18, -1.44869928e-20, 4.31033031e-23 };

		n2_out = n2_coef[0] + (n2_coef[1] * norm_n2) + (n2_coef[2] * pow(norm_n2, 2)) +
			(n2_coef[3] * pow(norm_n2, 3)) + (n2_coef[4] * pow(norm_n2, 4)) + (n2_coef[5] * pow(norm_n2, 5)) +
			(n2_coef[6] * pow(norm_n2, 6)) + (n2_coef[7] * pow(norm_n2, 7)) + (n2_coef[8] * pow(norm_n2, 8)) +
			(n2_coef[9] * pow(norm_n2, 9)) + (n2_coef[10] * pow(norm_n2, 10)) + (n2_coef[11] * pow(norm_n2, 11)) +
			(n2_coef[12] * pow(norm_n2, 12)) + (n2_coef[13] * pow(norm_n2, 13)) +
			(n2_coef[14] * pow(norm_n2, 14)) + (n2_coef[15] * pow(norm_n2, 15));

		n2_out = n2_out * n2;

		std::cout << "FADEC: idle= " << idleN2 << " Sim N2= " << n2 << " Pre N2= " << preN2 << " New N2= " << n2_out << std::flush;

		// Checking overshooting
		if (n2_out < preN2) {
			n2_out = preN2;
		}

		return n2_out;
	}

	double cegtNX(double cn1, double cff, double mach, double alt) {
		double cegt_out = 0;

		double cegt_coef[16] = {
			443.3145034,    0.0000000e+00,  3.0141710e+00,  3.9132758e-02,
			-4.8488279e+02, -1.2890964e-03, -2.2332050e-02, 8.3849683e-05,
			6.0478647e+00,  6.9171710e-05,  -6.5369271e-07, -8.1438322e-03,
			-5.1229403e-07, 7.4657497e+01,  -4.6016728e-03, 2.8637860e-08 };

		cegt_out = cegt_coef[0] + cegt_coef[1] + (cegt_coef[2] * cn1) +
			(cegt_coef[3] * cff) + (cegt_coef[4] * mach) +
			(cegt_coef[5] * alt) + (cegt_coef[6] * pow(cn1, 2)) +
			(cegt_coef[7] * cn1 * cff) + (cegt_coef[8] * cn1 * mach) +
			(cegt_coef[9] * cn1 * alt) + (cegt_coef[10] * pow(cff, 2)) +
			(cegt_coef[11] * mach * cff) + (cegt_coef[12] * cff * alt) +
			(cegt_coef[13] * pow(mach, 2)) +
			(cegt_coef[14] * mach * alt) + (cegt_coef[15] * pow(alt, 2));

		return cegt_out;
	}

	double cflowNX(double cn1, double mach, double alt) {
		double cflow_out = 0;

		double cflow_coef[21] = {
			-639.6602981, 0.00000e+00, 1.03705e+02,  -2.23264e+03, 5.70316e-03,
			-2.29404e+00, 1.08230e+02, 2.77667e-04,  -6.17180e+02, -7.20713e-02,
			2.19013e-07,  2.49418e-02, -7.31662e-01, -1.00003e-05, -3.79466e+01,
			1.34552e-03,  5.72612e-09, -2.71950e+02, 8.58469e-02,  -2.72912e-06,
			2.02928e-11 };

		// CRZ fuel cflow
		cflow_out =
			cflow_coef[0] + cflow_coef[1] + (cflow_coef[2] * cn1) +
			(cflow_coef[3] * mach) + (cflow_coef[4] * alt) +
			(cflow_coef[5] * pow(cn1, 2)) + (cflow_coef[6] * cn1 * mach) +
			(cflow_coef[7] * cn1 * alt) + (cflow_coef[8] * pow(mach, 2)) +
			(cflow_coef[9] * mach * alt) + (cflow_coef[10] * pow(alt, 2)) +
			(cflow_coef[11] * pow(cn1, 3)) + (cflow_coef[12] * pow(cn1, 2) * mach) +
			(cflow_coef[13] * pow(cn1, 2) * alt) +
			(cflow_coef[14] * cn1 * pow(mach, 2)) +
			(cflow_coef[15] * cn1 * mach * alt) +
			(cflow_coef[16] * cn1 * pow(alt, 2)) + (cflow_coef[17] * pow(mach, 3)) +
			(cflow_coef[18] * pow(mach, 2) * alt) +
			(cflow_coef[19] * mach * pow(alt, 2)) + (cflow_coef[20] * pow(alt, 3));

		return cflow_out;
	}
};
