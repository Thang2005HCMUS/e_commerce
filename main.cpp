#include <string.h>
#include <iostream>
#include <cstdint>
using namespace std;

int main() {
    // Thứ tự Little-Endian: byte thấp (4E) xếp trước, byte cao (00) xếp sau
    uint8_t a[4] = {0x4E, 0x61, 0xBC, 0x00};
    int b = 0;
    
    memcpy(&b, a, 4);
    cout << b << endl; // In ra chính xác: 12345678
    
    return 0;
}