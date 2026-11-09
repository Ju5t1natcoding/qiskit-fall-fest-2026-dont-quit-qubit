#include <bits/stdc++.h>
using namespace std;
using ll = long long;
using ull = unsigned long long;
using ld = long double;
#define all(v) begin(v), end(v)
#define al(v, l, r) begin(v) + l, begin(v) + r + 1
#define sz(v) static_cast<int>(v.size())
#define pb push_back
#define pob pop_back
#define fs first
#define sd second
#define HH (ct_h * H)

constexpr int inf = 2e9;
constexpr ll infll = 4e18;

template<typename T>
struct cplx {
    T x, y;

    cplx(T x = 0, T y = 0): x(x), y(y) {
    }

    friend cplx operator+(const cplx<T>& a, const cplx<T>& b) {
        cplx<T> rez;
        rez.x = a.x + b.x;
        rez.y = a.y + b.y;
        return rez;
    }

    friend cplx operator-(const cplx<T>& a, const cplx<T>& b) {
        cplx<T> rez;
        rez.x = a.x - b.x;
        rez.y = a.y - b.y;
        return rez;
    }

    friend cplx operator*(const cplx<T>& a, const cplx<T>& b) {
        cplx<T> rez;
        rez.x = a.x * b.x - a.y * b.y;
        rez.y = a.x * b.y + a.y * b.x;
        return rez;
    }

    friend istream& operator>>(istream& in, cplx<T>& z) {
        in >> z.x >> z.y;
        return in;
    }

    friend ostream& operator<<(ostream& out, const cplx<T>& z) {
        T y = z.y;
        bool neg = y < 0;

        if (neg) {
            y = -y;
        }

        out << z.x << (neg ? '-' : '+') << y << 'i';
        return out;
    }
};

template<typename T>
struct matrice {
    int n, m;
    vector<vector<cplx<T>>> v;

    matrice(int n, int m): n(n), m(m), v(n, vector<cplx<T>>(m)) {
    }

    matrice(int n, int m, vector<vector<cplx<T>>> v): n(n), m(m), v(v) {
    }

    friend matrice operator*(const matrice& a, const matrice& b) {
        if (a.m != b.n) {
            cout << "Pica inmultirea pe:\n" << a.n << " " << a.m << "\n";
            for (int i = 0; i < a.n; ++i) {
                for (int j = 0; j < a.m; ++j) {
                    cout << a.v[i][j] << " \n"[j == a.m - 1];
                }
            }

            cout << "\ncu:\n" << b.n << " " << b.m << "\n";
            for (int i = 0; i < b.n; ++i) {
                for (int j = 0; j < b.m; ++j) {
                    cout << b.v[i][j] << " \n"[j == b.m - 1];
                }
            }

            exit(0);
        }

        matrice rez(a.n, b.m);
        for (int k = 0; k < a.m; ++k) {
            for (int i = 0; i < a.n; ++i) {
                for (int j = 0; j < b.m; ++j) {
                    rez.v[i][j] = rez.v[i][j] + a.v[i][k] * b.v[k][j];
                }
            }
        }

        return rez;
    }

    friend matrice operator*(const cplx<T>& c, const matrice& a) {
        matrice rez = a;
        for (auto& v : rez.v) {
            for (auto& x : v) {
                x = c * x;
            }
        }

        return rez;
    }

    friend matrice prod_tensorial(const matrice& a, const matrice& b) {
        matrice rez(a.n * b.n, a.m * b.m);
        for (int i = 0; i < a.n; ++i) {
            for (int j = 0; j < a.m; ++j) {
                for (int p = 0; p < b.n; ++p) {
                    for (int q = 0; q < b.m; ++q) {
                        rez.v[i * b.n + p][j * b.m + q] = a.v[i][j] * b.v[p][q];
                    }
                }
            }
        }

        return rez;
    }

    friend istream& operator>>(istream& in, matrice& mat) {
        in >> mat.n >> mat.m;
        mat.v.assign(mat.n, vector<cplx<T>>(mat.m));

        for (int i = 0; i < mat.n; ++i) {
            for (int j = 0; j < mat.m; ++j) {
                in >> mat.v[i][j];
            }
        }

        return in;
    }

    friend ostream& operator<<(ostream& out, const matrice& mat) {
        out << mat.n << ' ' << mat.m << '\n';
        for (int i = 0; i < mat.n; ++i) {
            for (int j = 0; j < mat.m; ++j) {
                out << mat.v[i][j] << " \n"[j == mat.m - 1];
            }
        }

        return out;
    }
};

using M = matrice<double>;
using C = cplx<double>;

struct Ry_gate {
    const double& theta;

    M operator[](int t) {
        double a = theta * t / 2;
        return M(2, 2, {{cos(a), -sin(a)}, {sin(a), cos(a)}});
    }
};

signed main() {
    ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);

    M ket0(2, 1, {{1}, {0}}), ket1(2, 1, {{0}, {1}});
    double ct_h = 1 / sqrt(2.0); ///HH = poarta H
    M H(2, 2, {{1, 1}, {1, -1}});
    M X(2, 2, {{0, 1}, {1, 0}});
    M Z(2, 2, {{1, 0}, {0, -1}});
    M Y(2, 2, {{0, {0, -1}}, {{0, 1}, 0}}); /// (0 -i / i 0)
    double theta; ///unghiul pt matricea de rotatie
    Ry_gate Ry{theta}; ///Ry[t] = matricea de mai sus

    ///cod
}