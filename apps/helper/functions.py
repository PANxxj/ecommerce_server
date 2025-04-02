"""Response handing"""

class ResponseHandling:
    def failure_response_message(detail,result):
        """
        error message for failure
        :param detail: message to show in detail
        :param result : message or result to show
        :returns: dictionary
        """
        return {'status':False,'message' : detail, 'result' : result}

    def success_response_message(detail,result):
        """
        success message for Success
        :param detail: message to show in detail
        :param result : message or result to show
        :returns: dictionary
        """
        return {'status':True,'message' : detail, 'result' : result}

    def success_response_message_2(detail,result,cal_amounts):
        """
        success message for Success
        :param detail: message to show in detail
        :param result : message or result to show
        :returns: dictionary
        """
        return {'status':True,'message' : detail, 'result' : result,'cal_amounts':cal_amounts}
    
    def error_message(msg):
        return {'status':False,'message':msg}
    
    def success_message(msg):
        return {'status':True,'message':msg}
    
    
#------------------------- ERROR GENERAL FUNCTIONS ------------------------------------

def error_message_function(errors):
    """
    return error message when serializer is not valid
    :param errors: error object
    :returns: string
    """
    for key, values in errors.items():
        error = [value[:] for value in values]
        err = ' '.join(map(str,error))
        return err


def return_steps():
    return [
        {
            "id": 1,
            "status": "Order Placed",
            "description": "Your order has been received and is being processed.",
            "date": "2023-10-25",
            "time": "09:23 AM",
            "completed": True
        },
        {
            "id": 2,
            "status": "Processing",
            "description": "Your order is being prepared for shipping.",
            "date": "2023-10-25",
            "time": "02:45 PM",
            "completed": True
        },
        {
            "id": 3,
            "status": "Shipped",
            "description": "Your order has been shipped and is on its way to you.",
            "date": "2023-10-26",
            "time": "11:30 AM",
            "completed": True
        },
        {
            "id": 4,
            "status": "Out for Delivery",
            "description": "Your package is out for delivery and will arrive today.",
            "date": "2023-10-27",
            "time": "08:15 AM",
            "completed": False
        },
        {
            "id": 5,
            "status": "Delivered",
            "description": "Your package has been delivered.",
            "date": "Pending",
            "time": "Pending",
            "completed": False
        }
    ]