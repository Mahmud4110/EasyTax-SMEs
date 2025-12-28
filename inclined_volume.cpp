#include <iostream>
#include <cmath>
#include <vector>
#include <iomanip>

using namespace std;

// ====================================================
// Circular segment area
// ====================================================
double segment_area(double h, double R)
{
    // Clip to physical limits
    if (h >= R) return M_PI * R * R;
    if (h <= -R) return 0.0;

    return R * R * acos(-h / R) - h * sqrt(R * R - h * h);
}

// ====================================================
// Adaptive Simpson integration
// ====================================================
double simpson(double f(double, double), double a, double b, double R)
{
    double c = 0.5 * (a + b);
    return (b - a) / 6.0 * (f(a, R) + 4.0 * f(c, R) + f(b, R));
}

double adaptive_simpson(double f(double, double),
                        double a, double b,
                        double eps,
                        double whole,
                        double R,
                        int depth)
{
    double c = 0.5 * (a + b);
    double left  = simpson(f, a, c, R);
    double right = simpson(f, c, b, R);

    if (depth <= 0 || fabs(left + right - whole) < 15 * eps)
        return left + right + (left + right - whole) / 15.0;

    return adaptive_simpson(f, a, c, eps / 2, left, R, depth - 1) +
           adaptive_simpson(f, c, b, eps / 2, right, R, depth - 1);
}

double integrate(double f(double, double),
                 double a, double b,
                 double R)
{
    double whole = simpson(f, a, b, R);
    return adaptive_simpson(f, a, b, 1e-9, whole, R, 20);
}

// ====================================================
// Exact inclined cylinder volume
// ====================================================
double exact_volume(double b, double R, double H, double m)
{
    if (fabs(m) < 1e-12)
    {
        return H * segment_area(b, R);
    }
    else
    {
        double h1 = b - m * H;
        double h2 = b;
        return integrate(segment_area, h1, h2, R) / m;
    }
}

// ====================================================
// Root finding (bisection – robust like brentq)
// ====================================================
double find_b(double R, double H, double m, double V_target)
{
    double V_full = M_PI * R * R * H;
    double b_min = -R;
    double b_max = R + m * H;

    auto F = [&](double b)
    {
        return exact_volume(b, R, H, m) - V_target;
    };

    double lo = b_min;
    double hi = b_max;

    for (int i = 0; i < 80; i++)
    {
        double mid = 0.5 * (lo + hi);
        if (F(lo) * F(mid) <= 0)
            hi = mid;
        else
            lo = mid;
    }

    return 0.5 * (lo + hi);
}

// ====================================================
// Main
// ====================================================
int main()
{
    double R = 37.5;
    double H = 100.0;
    double V_target = 58315.81;  // cm^3

    vector<double> alpha_list =
    {
        89.9, 80, 70, 60, 50, 40, 30, 20, 10, 0.1
    };

    cout << fixed << setprecision(6);
    cout << " Alpha (deg) |        b (cm) |      Volume (cm^3)\n";
    cout << "---------------------------------------------------\n";

    for (double alpha_deg : alpha_list)
    {
        double m = tan(alpha_deg * M_PI / 180.0);
        double b = find_b(R, H, m, V_target);
        double V = exact_volume(b, R, H, m);

        cout << setw(11) << alpha_deg << " | "
             << setw(13) << b << " | "
             << setw(15) << V << "\n";
    }

    return 0;
}
