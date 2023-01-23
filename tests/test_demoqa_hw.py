import allure
from selene import have
from selene import command
import os


def test_demoqa_hw(setup_chrome):
    browser = setup_chrome
    with allure.step('Открываем страницу формы'):
        browser.open('https://demoqa.com/automation-practice-form')

    with allure.step('Убираем рекламу'):
        browser.all('[id^=google_ads][id$=container__]').with_(timeout=5).wait_until(have.size_greater_than_or_equal(3))
        browser.all('[id^=google_ads][id$=container__]').perform(command.js.remove)

    with allure.step('Заполняем форму данными'):
        browser.element('#firstName').type('Alex')
        browser.element('#lastName').type('Alekseev')
        browser.element('#userEmail').type('alexalekseev@gmail.com')

        browser.all('[name=gender]').element_by(have.value('Male')).element('..').click()
        browser.element('#userNumber').type('8910123121')

        browser.element('#dateOfBirthInput').click()
        browser.element('.react-datepicker__month-select').send_keys('May')
        browser.element('.react-datepicker__year-select').send_keys('1991')
        browser.element(f'.react-datepicker__day--00{7}').click()

        browser.element('#subjectsInput').type('History').press_enter()
        browser.element('[type=checkbox][id=hobbies-checkbox-3]+label').should(
            have.exact_text('Music')).click()

    with allure.step('Загружаем картинку'):
        browser.element('#uploadPicture').set_value(
            os.path.abspath(
                os.path.join(os.path.dirname(__file__), 'resources/Photo_test_yellow.png')
            )
        )

    with allure.step('Заполняем поля адреса'):
        browser.element('#currentAddress').perform(command.js.set_value(
            'Delhi, Pyatnitskaya st 12/12'))
        browser.element('#react-select-3-input').send_keys('NCR').press_enter()
        browser.element('#react-select-4-input').send_keys('Delhi').press_enter()

        browser.element('#submit').perform(command.js.click)

    with allure.step('Проверяем заполненные данные'):
        browser.all('.table-responsive td:nth-child(2)').should(have.texts(
            'Alex Alekseev', 'alexalekseev@gmail.com', 'Male', '8910123121',
            '07 May,1991', 'History', 'Music', 'Photo_test_yellow.png',
            'Delhi, Pyatnitskaya st 12/12', 'NCR Delhi'))
