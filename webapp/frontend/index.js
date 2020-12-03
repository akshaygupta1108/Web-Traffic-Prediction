const INVALID_SELECTION_MESSAGE = "Please make a valid selection";
const FETCHING_RESULTS_MESSAGE = "Fetching the results";
const ERROR_MESSAGE = "Error fetching the results!";
const MODEL_ALREADY_SELECTED_MESSAGE= "This model is already selected!";

const MODEL_TEXT = "Model Selected: ";
const ACCURACY_TEXT = "The Loss(RMSE) of the selected model is: ";

const NEXT_DAY = 1;
const NEXT_WEEK = 7;
const NEXT_MONTH = 30;

const ARIMA = 'ARIMA';
const LSTM = 'LSTM';
const CNN = 'CNN';

const API_URL = "http:/localhost:5000/";

/**
 * json response contains - 
 *      predictionLink
 *      loss
 *      graphImageSource
 */

function refreshModelData(){
    var json = JSON.parse(localStorage.getItem('json_response'));
    if(json['error']==ERROR_MESSAGE){
        return;
    }
    var params = JSON.parse(localStorage.getItem('params'));
    document.getElementById("predictionLink").href = json['predictionLink'];

    document.getElementById("model_selected_text").innerHTML = MODEL_TEXT + params['model'];
    document.getElementById("accuracy_text").innerHTML = ACCURACY_TEXT + json['loss'];
    document.getElementById("graph_image").src = json['graphImageSource'];

}

function getResults(){
    console.log("getting results");
    if(!localStorage.getItem('params')){
        alert(INVALID_SELECTION_MESSAGE);
        return;
    }
    var params = JSON.parse(localStorage.getItem('params'));
    var searchWord = params['searchWord'];
    var model = params['model'];
    var forecastDays = params['forecastDays'];
    var language = params['language'];
    var access = params['access'];
    alert(FETCHING_RESULTS_MESSAGE);
    
    var api_url = API_URL + model + '/' + searchWord + '/' + language + '/' + forecastDays + '/' + access;
    console.log(api_url);

    fetch(api_url)
    .then(response => response.json())
    .then(json =>{
        localStorage.setItem('json_response',JSON.stringify(json));
        // alert(localStorage.getItem('params'));
        // alert(localStorage.getItem('json_response'));
        refreshModelData();
    })
    .catch(() => {
        alert(ERROR_MESSAGE);
        localStorage.clear();
    });
}

function submitSearch(){
    console.log("button pressed");
    var params = JSON.parse(localStorage.getItem('params'));
    if(!params){
        var searchWord = ""+document.getElementById("searchField").value;
        var model = ARIMA;
        var forecastDays = NEXT_WEEK;
        var language = ""+document.getElementById("languageSelect").value;
        var access = ""+document.getElementById("accessSelect").value;
        params = {'searchWord':searchWord,'model':model,'forecastDays':forecastDays, 'language':language, 'access':access};
    }
    else{
        var searchWord = ""+document.getElementById("searchField").value;
        var language = ""+document.getElementById("languageSelect").value;
        var access = ""+document.getElementById("accessSelect").value;
        params['searchWord'] = searchWord;
        params['language'] = language;
        params['access'] = access;
    }
    localStorage.setItem('params',JSON.stringify(params));
    getResults();
}

function changeModelType(model){
    var params = JSON.parse(localStorage.getItem('params'));
    if(!params){
        alert(INVALID_SELECTION_MESSAGE);
        return;
    }
    if(params['model'] == model){
        alert(MODEL_ALREADY_SELECTED_MESSAGE);
        return;
    }
    params['model'] = model;
    localStorage.setItem('params',JSON.stringify(params));
    getResults();
}

function changeModelToLSTM(){
    changeModelType(LSTM);
}

function changeModelToARIMA(){
    changeModelType(ARIMA);
}

function changeModelToCNN(){
    changeModelType(CNN);
}

function changeForecastDays(days){
    var params = JSON.parse(localStorage.getItem('params'));
    if(!params){
        alert(INVALID_SELECTION_MESSAGE);
        return;
    }
    if(params['forecastDays'] == days){
        alert(MODEL_ALREADY_SELECTED_MESSAGE);
        return;
    }
    params['forecastDays'] = days;
    localStorage.setItem('params',JSON.stringify(params));
    getResults();
}

function changeModelToNextDay(){
    changeForecastDays(NEXT_DAY);
}

function changeModelToNextWeek(){
    changeForecastDays(NEXT_WEEK);
}

function changeModelToNextMonth(){
    changeForecastDays(NEXT_MONTH);
}