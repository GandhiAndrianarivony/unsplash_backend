import typing
import torch


def predict(
    model: torch.nn.Module, data, categories: typing.List[str]
) -> typing.Tuple[int, int]:
    model = model.to("cpu")

    model.eval()
    with torch.inference_mode():
        pred_logit = model(data)

        # Conver prediction to probability using softmax
        pred_proba = torch.softmax(pred_logit, dim=1)
        pred_label = torch.argmax(pred_proba, dim=1)
    
    pred_proba = pred_proba.squeeze()
    category_name = categories[pred_label.item()]
    print(f"Category: {category_name} --> {100 * pred_proba[pred_label].item(): .1f}%")
    return category_name
