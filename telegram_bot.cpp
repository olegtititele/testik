#include <stdio.h>
#include <tgbot/tgbot.h>

#include <string>
#include <vector>
#include <curl/curl.h>
#include <map>

#include <fstream>
#include <iterator>

#include "config.h"


using namespace std;
using namespace TgBot;

// static size_t Writer(char *buffer, size_t size, size_t nmemb, string *html){
//     int result = 0;

//     if(buffer != NULL){
//         html->append(buffer, size*nmemb);
//         result = size*nmemb;
//     }
//     return result;
// }

// string get_request(string link){
//     CURL *curl;
//     string data;
//     curl = curl_easy_init();
//     curl_easy_setopt(curl,CURLOPT_URL, link.c_str());
//     curl_easy_setopt(curl,CURLOPT_WRITEFUNCTION,Writer);
//     curl_easy_setopt(curl,CURLOPT_WRITEDATA,&data);
//     curl_easy_perform(curl);
//     curl_easy_cleanup(curl);
//     return data;
// }

bool check_sub_channel(string chat_member)
{
    if (chat_member != "left"){
        return true;
    }else{
        return false;
    }

};


int main() {

    Bot bot(bot_token);
    state = 0;
    ForceReply::Ptr save_link;

    InlineKeyboardMarkup::Ptr keyboard(new InlineKeyboardMarkup);
    InlineKeyboardMarkup::Ptr countries_kb(new InlineKeyboardMarkup);
    InlineKeyboardMarkup::Ptr contacts_kb(new InlineKeyboardMarkup);
    InlineKeyboardMarkup::Ptr settings_kb(new InlineKeyboardMarkup);

    // Клавиатура меню
    int rows = sizeof(main_memu_buttons) / sizeof(*main_memu_buttons);
    for (int row = 0; row < rows; row++) 
    {   
        vector<InlineKeyboardButton::Ptr> buttons;
        InlineKeyboardButton::Ptr btn(new InlineKeyboardButton);
        btn->text = main_memu_buttons[row];
        btn->callbackData = main_menu_calldata[row];
        buttons.push_back(btn);
        keyboard->inlineKeyboard.push_back(buttons); 
    }
    
    // Клавиатура стран
    for(auto& el : countries_sites)
    {
        vector<InlineKeyboardButton::Ptr> countries_buttons;
        InlineKeyboardButton::Ptr btn(new InlineKeyboardButton);
        btn->text = el.first;
        btn->callbackData = el.second;
        countries_buttons.push_back(btn);
        countries_kb->inlineKeyboard.push_back(countries_buttons);
    }
    vector<InlineKeyboardButton::Ptr> countries_buttons;
    InlineKeyboardButton::Ptr back_btn(new InlineKeyboardButton);
    back_btn->text = "🔙 Вернуться в меню";
    back_btn->callbackData = "back_to_menu";
    countries_buttons.push_back(back_btn);
    countries_kb->inlineKeyboard.push_back(countries_buttons);

    // Клавиатура настроек
    vector<InlineKeyboardButton::Ptr> settings_buttons;
    InlineKeyboardButton::Ptr btn(new InlineKeyboardButton);
    for(auto& el : filters_buttons)
    {
        btn->text = el.first;
        btn->callbackData = el.second;
        settings_buttons.push_back(btn);
    }
    settings_kb->inlineKeyboard.push_back(settings_buttons);

    vector<InlineKeyboardButton::Ptr> back_buttons;
    InlineKeyboardButton::Ptr back_button(new InlineKeyboardButton);
    back_button->text = "🔙 Вернуться в меню";
    back_button->callbackData = "back_to_menu";
    back_buttons.push_back(back_button);
    settings_kb->inlineKeyboard.push_back(back_buttons);


    // Клавиатура информации
    contacts_kb->inlineKeyboard.push_back(back_buttons);
   
    bot.getEvents().onCommand("start", [&bot, &keyboard](Message::Ptr message) {
        if(check_sub_channel(bot.getApi().getChatMember(news_channel_chat_id, message->chat->id)->status)){
            bot.getApi().sendMessage(message->chat->id, "🆔 <b>Ваш ид:</b> <code>"+to_string(message->chat->id)+"</code>\n💰 <b>Ваш баланс:</b> <code>350 ₽</code>", true, 0, keyboard, "HTML", false);
        }else{
            bot.getApi().sendMessage(message->chat->id, "🆘 <b>Вас нет в канале <a href=\""+news_channel+"\">новостей</a>. Вступите, чтобы пользоваться ботом.</b>", false, 0,0, "HTML");
        }
    });
    bot.getEvents().onCallbackQuery([&bot, &keyboard, &countries_kb, &contacts_kb, &settings_kb, &save_link](CallbackQuery::Ptr query){
        for(auto& el : countries_sites){
            if (query->data == el.second){
                state = 1;
                bot.getApi().editMessageText("Введите ссылку", query->message->chat->id, query->message->messageId, "","HTML", true, save_link);
            };
        }   
    
        if (query->data == "show_services"){ //Посмотреть все сервисы
            bot.getApi().editMessageText("<b>🌐 Выберите площадку, где вы хотите найти объявления.</b>", query->message->chat->id, query->message->messageId, "","HTML", true, countries_kb);
        }else if (query->data == "previously_added"){ //Ранее добаленные
            cout << "pops";
            // bot.getApi().editMessageCaption(query->message->chat->id, query->message->messageId, "🌐 Выберите площадку, где вы хотите найти объявления.", "",countries_kb);
        }else if (query->data == "back_to_menu"){  //Вернуться в меню
            bot.getApi().editMessageText("🆔 <b>Ваш ид:</b> <code>"+to_string(query->message->chat->id)+"</code>\n💰 <b>Ваш баланс:</b> <code>350 ₽</code>", query->message->chat->id, query->message->messageId, "","HTML", true, keyboard); 
        }else if (query->data == "info"){
            bot.getApi().editMessageText("<b>Контакты </b><a href=\"t.me/dvablanta\">GUESS</a>\n<b>Канал новостей</b> <a href=\""+news_channel+"\">GzuzPars News</a>", query->message->chat->id, query->message->messageId, "","HTML", true, contacts_kb);
        }else if (query->data == "settings"){
            bot.getApi().editMessageText("<b>🖋 Выберите пункт который хотите изменить.</b>", query->message->chat->id, query->message->messageId, "","HTML", true, settings_kb);
        }
    });

    bot.getEvents().onAnyMessage([&bot, &save_link](Message::Ptr message) {
        printf("User wrote %s\n", message->text.c_str());
        if (StringTools::startsWith(message->text, "/start")) {
            return;
        }else if (state=1){
            bot.getApi().sendMessage(message->chat->id, "Ваша ссылка: " + message->text);
            state = 0;
        }
        cout << "kakash";
        // bot.getApi().sendMessage(message->chat->id, "Your messbthtage is: " + message->text);
    });

    try {
        printf("Bot username: %s\n", bot.getApi().getMe()->username.c_str());
        TgLongPoll longPoll(bot);
        while (true) {
            printf(bot.getApi().);
            longPoll.start();
        }
    } catch (TgException& e) {
        printf("error: %s\n", e.what());
    }
    return 0;
}