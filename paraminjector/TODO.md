## Static ParamInjector

### Phases:
1. User creates instance and passes passes func along with a list of **combinations** of argument types and
 corresponding objects or callables for dynamic initialization
```
inj = ParamInjector([
    {HTMLBuilder, MenuBuilder, MetaBuilder}, 
    {HTMLBuilder, ReplyMarkupBuilder},
])
```
1. Analyze signature and determine which of the combinations will fit
1. User can call `prepare` method to initialize arguments that will change for every invocation:
```
ready_executor = inj.prepare({
    MyObject: something_initialized_dynamically
}).fire()
```

