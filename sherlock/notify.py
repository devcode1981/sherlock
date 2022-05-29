"""Sherlock Notify Module

This module defines the objects for notifying the caller about the
results of queries.
"""
from result import QueryStatus
from colorama import Fore, Style


class QueryNotify:
    """Query Notify Object.

    Base class that describes methods available to notify the results of
    a query.
    It is intended that other classes inherit from this base class and
    override the methods to implement specific functionality.
    """

    def __init__(self, result=None):
        """Create Query Notify Object.

        Contains information about a specific method of notifying the results
        of a query.

        Keyword Arguments:
        self                   -- This object.
        result                 -- Object of type QueryResult() containing
                                  results for this query.

        Return Value:
        Nothing.
        """

        self.result = result

        # return

    def start(self, message=None):
        """Notify Start.

        Notify method for start of query.  This method will be called before
        any queries are performed.  This method will typically be
        overridden by higher level classes that will inherit from it.

        Keyword Arguments:
        self                   -- This object.
        message                -- Object that is used to give context to start
                                  of query.
                                  Default is None.

        Return Value:
        Nothing.
        """

        # return

    def update(self, result):
        """Notify Update.

        Notify method for query result.  This method will typically be
        overridden by higher level classes that will inherit from it.

        Keyword Arguments:
        self                   -- This object.
        result                 -- Object of type QueryResult() containing
                                  results for this query.

        Return Value:
        Nothing.
        """

        self.result = result

        # return

    def finish(self, message=None):
        """Notify Finish.

        Notify method for finish of query.  This method will be called after
        all queries have been performed.  This method will typically be
        overridden by higher level classes that will inherit from it.

        Keyword Arguments:
        self                   -- This object.
        message                -- Object that is used to give context to start
                                  of query.
                                  Default is None.

        Return Value:
        Nothing.
        """

        # return

    def __str__(self):
        """Convert Object To String.

        Keyword Arguments:
        self                   -- This object.

        Return Value:
        Nicely formatted string to get information about this object.
        """
        return str(self.result)


class QueryNotifyPrint(QueryNotify):
    """Query Notify Print Object.

    Query notify class that prints results.
    """

    def __init__(self, result=None, verbose=False, print_all=False):
        """Create Query Notify Print Object.

        Contains information about a specific method of notifying the results
        of a query.

        Keyword Arguments:
        self                   -- This object.
        result                 -- Object of type QueryResult() containing
                                  results for this query.
        verbose                -- Boolean indicating whether to give verbose output.
        print_all              -- Boolean indicating whether to only print all sites, including not found.

        Return Value:
        Nothing.
        """

        super().__init__(result)
        self.verbose = verbose
        self.print_all = print_all

        return

    def start(self, message):
        """Notify Start.

        Will print the title to the standard output.

        Keyword Arguments:
        self                   -- This object.
        message                -- String containing username that the series
                                  of queries are about.

        Return Value:
        Nothing.
        """

        title = "Checking username"

        print(Style.BRIGHT + Fore.GREEN + "[" +
              Fore.YELLOW + "*" +
              Fore.GREEN + f"] {title}" +
              Fore.WHITE + f" {message}" +
              Fore.GREEN + " on:")
        # An empty line between first line and the result(more clear output)
        print('\r')

        return

    def finish(self, message="The processing has been finished."):
        """Notify Start.

        Will print the last line to the standard output.

        Keyword Arguments:
        self                   -- This object.
        message                -- The last phrase.

        Return Value:
        Nothing.
        """

        title = "End"
        
        print('\r') # An empty line between last line of main output and last line(more clear output)
        print(Style.BRIGHT + Fore.GREEN + "[" +
              Fore.YELLOW + "!" +
              Fore.GREEN + f"] {title}" +
              Fore.GREEN + ": " +
              Fore.WHITE + f" {message}" )
              
        # An empty line between first line and the result(more clear output)

        # return

    def update(self, result):
        """Notify Update.

        Will print the query result to the standard output.

        Keyword Arguments:
        self                   -- This object.
        result                 -- Object of type QueryResult() containing
                                  results for this query.

        Return Value:
        Nothing.
        """
        self.result = result

        response_time_text = ""
        if self.result.query_time is not None and self.verbose == True:
            response_time_text = f" [{round(self.result.query_time * 1000)}ms]"
        
        # Output to the terminal is desired.
        if result.status == QueryStatus.CLAIMED:
            print(Style.BRIGHT + Fore.WHITE + "[" +
                  Fore.GREEN + "+" +
                  Fore.WHITE + "]" +
                  response_time_text +
                  Fore.GREEN +
                  f" {self.result.site_name}: " +
                  Style.RESET_ALL +
                  f"{self.result.site_url_user}")

        elif result.status == QueryStatus.AVAILABLE:
            if self.print_all:
                print(Style.BRIGHT + Fore.WHITE + "[" +
                      Fore.RED + "-" +
                      Fore.WHITE + "]" +
                      response_time_text +
                      Fore.GREEN + f" {self.result.site_name}:" +
                      Fore.YELLOW + " Not Found!")

        elif result.status == QueryStatus.UNKNOWN:
            if self.print_all:
                print(Style.BRIGHT + Fore.WHITE + "[" +
                      Fore.RED + "-" +
                      Fore.WHITE + "]" +
                      Fore.GREEN + f" {self.result.site_name}:" +
                      Fore.RED + f" {self.result.context}" +
                      Fore.YELLOW + f" ")

        elif result.status == QueryStatus.ILLEGAL:
            if self.print_all:
                msg = "Illegal Username Format For This Site!"
                print(Style.BRIGHT + Fore.WHITE + "[" +
                      Fore.RED + "-" +
                      Fore.WHITE + "]" +
                      Fore.GREEN + f" {self.result.site_name}:" +
                      Fore.YELLOW + f" {msg}")

        else:
            # It should be impossible to ever get here...
            raise ValueError(
                f"Unknown Query Status '{result.status}' for site '{self.result.site_name}'"
            )

        return
    
    def finish(self, message="The processing has been finished."):
        """Notify Start.
        Will print the last line to the standard output.
        Keyword Arguments:
        self                   -- This object.
        message                -- The last phrase.
        Return Value:
        Nothing.
        """

        title = "End"
        
        print('\r') # An empty line between last line of main output and last line(more clear output)
        print(Style.BRIGHT + Fore.GREEN + "[" +
              Fore.YELLOW + "!" +
              Fore.GREEN + f"] {title}" +
              Fore.GREEN + ": " +
              Fore.WHITE + f" {message}" )
              
        # An empty line between first line and the result(more clear output)

        return

    def __str__(self):
        """Convert Object To String.

        Keyword Arguments:
        self                   -- This object.

        Return Value:
        Nicely formatted string to get information about this object.
        """
        return str(self.result)
