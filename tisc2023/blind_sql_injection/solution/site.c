#include <stdio.h>
#include <stdlib.h>
#include <emscripten.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int hex_to_int(char c) {
    if (c >= '0' && c <= '9') {
        return c - '0';
    } else if (c >= 'A' && c <= 'F') {
        return c - 'A' + 10;
    } else if (c >= 'a' && c <= 'f') {
        return c - 'a' + 10;
    }
    return -1;
}

void utf8_encode(char* dest, uint32_t codepoint) {
    if (codepoint <= 0x7F) {
        *dest++ = (char)codepoint;
    } else if (codepoint <= 0x7FF) {
        *dest++ = (char)((codepoint >> 6) | 0xC0);
        *dest++ = (char)((codepoint & 0x3F) | 0x80);
    } else if (codepoint <= 0xFFFF) {
        *dest++ = (char)((codepoint >> 12) | 0xE0);
        *dest++ = (char)(((codepoint >> 6) & 0x3F) | 0x80);
        *dest++ = (char)((codepoint & 0x3F) | 0x80);
    } else if (codepoint <= 0x10FFFF) {
        *dest++ = (char)((codepoint >> 18) | 0xF0);
        *dest++ = (char)(((codepoint >> 12) & 0x3F) | 0x80);
        *dest++ = (char)(((codepoint >> 6) & 0x3F) | 0x80);
        *dest++ = (char)((codepoint & 0x3F) | 0x80);
    }
}

void url_decode(char* dest, const char* src) {
    while (*src) {
        if (*src == '%') {
            int d1 = hex_to_int(*(src + 1));
            int d2 = hex_to_int(*(src + 2));
            if (d1 != -1 && d2 != -1) {
                uint32_t codepoint = (d1 << 4) + d2;
                src += 3;

                utf8_encode(dest, codepoint);
                dest += strlen(dest);
            } else {
                *dest++ = *src++;
            }
        } else {
            *dest++ = *src++;
        }
    }
    *dest = '\0';
}

void format_strings(const char *username, const char *password, char *result, size_t size) {
    snprintf(result, size, "SELECT * from Users WHERE username=\"%s\" AND password=\"%s\"", username, password);
}

const char* EMSCRIPTEN_KEEPALIVE load_query(const char* username, const char* password) {
  static char result[300];
  format_strings(username, password, result, sizeof(result));
  return result;
}

bool is_alpha(const char *str) {
    while (*str) {
        if (!isalpha(*str)) {
            return false;
        }
        str++;
    }
    return true;
}

const char* EMSCRIPTEN_KEEPALIVE is_blacklisted(const char* username, const char* password) {
      if (!is_alpha(username) || !is_alpha(password)) {
        return "Blacklisted!";
    } else {
        return load_query(username, password);
    }
}

const char* EMSCRIPTEN_KEEPALIVE craft_query(char *username_str, char *password_str) {
  void *func_ptr;
  char username[60];
  char password[60];
  func_ptr = is_blacklisted;
  int a = (int)is_blacklisted;
  int b = (int)load_query;
  
  url_decode(username, username_str);
  
  strncpy(password, password_str, 59);
  password[59] = '\0';

  return ((const char* (*)(char*, char*))func_ptr)(username, password); //execute function of pointer
}
