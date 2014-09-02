<?php

namespace App\Factories;

use Nette,
	App,
	App\Database\Entities\GalleryEntity;

/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
final class ManageGalleryFormFactory extends Nette\Object
{
	use TFormSaveHandlers;


	/** @var App\Factories\FormFactory */
	private $formFactory;

	/** @var App\Database\Entities\GalleryEntity */
	private $galleryEntity;

	/** @var Nette\Database\Table\ActiveRow */
	private $row;


	public function __construct(
		FormFactory $formFactory,
		GalleryEntity $galleryEntity
	) {
		$this->formFactory = $formFactory;
		$this->galleryEntity = $galleryEntity;
	}


	public function create($offerId, $id)
	{
		if ($id) {
			$this->row = $this->galleryEntity->find($id);
		}

		$form = $this->formFactory->create();

		$form->addHidden("offer_id", $offerId);

		$form->addText("name", "Název", 50, 50)
			->setRequired("Název je povinný!");

		$form->addTextarea("text", "Text", 50, 4)
			->setAttribute("class", "ckeditor");

		$form->addSubmit("send", $this->row ? "Upravit" : "Přidat")
			->setAttribute("class", "btn-primary")
			->onClick[] = $this->save;

		if ($this->row) {
			$form->addSubmit("sendAndContinue", "Uložit a pokračovat v editaci")
				->setAttribute("class", "btn-primary")
				->onClick[] = $this->saveAndContinue;
		}

		return $form;
	}


	public function process(Nette\Application\UI\Form $form)
	{
		$values = $form->getValues(true);

		if (!$values["offer_id"]) {
			unset ($values["offer_id"]);
		}

		if (!$this->row) {
			$values["ins_process"] = __METHOD__;
			$this->galleryEntity->insert($values);
		} else {
			$values["upd_process"] = __METHOD__;
			$this->row->update($values);
		}

	}

}
