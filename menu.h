 #include <Arduino.h>

typedef void (*fptr)(void);

class MenuItem{
  private:
    const char* text;
    fptr callback;
  public:
    MenuItem(const char* text, fptr callback);
    const char* getText();
    fptr getCallback();
  };


class Menu{

  private:
    uint8_t index;
    uint8_t n_items;
    MenuItem *items[10];
    Stream *MenuStream;
  public:
    Menu();
    void begin(Stream &s);
    void addItem(const char* text, fptr callback);
    void up();
    void down();
    void enter();
  };
