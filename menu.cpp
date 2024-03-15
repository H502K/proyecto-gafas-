#include "menu.h"

MenuItem::MenuItem(const char* text, fptr callback):
  text(text),
  callback(callback)
{}

const char* MenuItem::getText(){
  return text;

}

fptr MenuItem::getCallback(){
return callback;

}

Menu::Menu() {
  index = 0;
  n_items = 0;
  MenuStream = NULL;
}


void Menu::begin(Stream &s){
    MenuStream = &s;
  }

void Menu::addItem(const char* text, fptr callback) {
  if (n_items < 10) {
    items[n_items] = new MenuItem(text, callback);
    n_items++;
  }
}

void Menu::up() {
  if (index < n_items - 1) {
    index++;
    if(MenuStream != NULL)
    MenuStream->println(items[index]->getText());
  }
}

void Menu::down() {
  if (index > 0) {
    index--;
    if(MenuStream != NULL)
    MenuStream->println(items[index]->getText());
  }
}

void Menu::enter() {
  fptr callback = items[index]->getCallback();
  if (callback != NULL) callback();
}
