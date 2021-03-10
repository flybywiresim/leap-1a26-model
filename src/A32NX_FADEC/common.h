#ifndef _COMMON_H_
#define _COMMON_H_

class SimVars;

/// <summary>
/// The handle to the SimConnect instance.
/// </summary>
HANDLE hSimConnect;

/// <summary>
/// The environmental corrected ratios
/// </summary>
class Ratios
{
public:
	SimVars* simVars;

	FLOAT64 theta() {
		double t = (288.15 - (1.98 * this->simVars->getPlaneAltitude() / 1000)) / 288.15;
		return t;
	}

	FLOAT64 delta() {
		double d = pow(this->theta(), 5.256);
		return d;
	}

	FLOAT64 theta2() {
		double t2 = this->theta() * (1 + 0.2 * pow(this->simVars->getMach(), 2));
		return t2;
	}

	FLOAT64 delta2() {
		double d2 = this->delta() * pow((1 + 0.2 * pow(this->simVars->getMach(), 2)), 3.5);
		return d2;
	}
};

//class Debug
//{
//public:
//	void text(std::string msg) {
//		std::ofstream outfile;
//		outfile.open("\\work\\test.txt", std::ios::app); // append instead of overwrite
//		//outfile << msg << std::flush;
//		outfile.close();
//	}
//};

template<typename T/*, typename = std::enable_if_t<std::is_integral_v<T>>*/>
std::string to_string_with_zero_padding(const T& value, std::size_t total_length)
{
	auto str = std::to_string(value);
	if (str.length() < total_length)
		str.insert(str.front() == '-' ? 1 : 0, total_length - str.length(), '0');
	return str;
}
#endif